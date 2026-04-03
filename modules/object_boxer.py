from PIL import Image, ImageDraw
from modules.background_remover import BackgroundRemover
from modules.grayscale_converter import GrayscaleConverter

class ObjectBoxer:
    def __init__(self):
        self.result_image = None
        self.object_area = 0
        self.objects = []  # list of dicts: {'bbox', 'centroid', 'area'}

    def box_objects(self, pil_image, threshold=128):
        """
        Detect objects using BackgroundRemover to get foreground mask,
        then draw bounding boxes and set background to grayscale
        using GrayscaleConverter.
        Returns (image, total_object_pixels).
        """
        # Use BackgroundRemover to obtain RGBA image with foreground opaque
        bg_remover = BackgroundRemover()
        rgba_img = bg_remover.remove_background(pil_image, tolerance=30)
        if rgba_img is None:
            raise Exception("Background removal failed – cannot detect objects")

        width, height = rgba_img.size
        # Build foreground mask from alpha channel (alpha > 0)
        fg_mask = [[0 for _ in range(width)] for _ in range(height)]
        pixels = rgba_img.load()
        for y in range(height):
            for x in range(width):
                if pixels[x, y][3] > 0:
                    fg_mask[y][x] = 1

        # Connected component labeling
        objects = self._label_components(fg_mask)

        total_object_pixels = sum(obj['area'] for obj in objects)
        self.object_area = total_object_pixels
        self.objects = objects

        # Create a full grayscale version of the original image using GrayscaleConverter
        converter = GrayscaleConverter()
        grayscale_full = converter.convert_to_grayscale(pil_image)  # returns RGB with R=G=B

        # Build result image: start with the grayscale image, then copy original colors over foreground
        # This avoids a separate grayscale loop – we just use the precomputed grayscale image.
        if grayscale_full.mode != 'RGB':
            grayscale_full = grayscale_full.convert('RGB')
        result = grayscale_full.copy()
        result_pixels = result.load()

        # If the original image is not RGB, convert a copy for color extraction
        if pil_image.mode != 'RGB':
            original_rgb = pil_image.convert('RGB')
        else:
            original_rgb = pil_image
        original_pixels = original_rgb.load()

        # Restore original colours for foreground pixels
        for y in range(height):
            for x in range(width):
                if fg_mask[y][x] == 1:
                    result_pixels[x, y] = original_pixels[x, y]

        # Draw bounding boxes
        draw = ImageDraw.Draw(result)
        for obj in objects:
            x1, y1, x2, y2 = obj['bbox']
            draw.rectangle([x1, y1, x2, y2], outline='red', width=2)

        self.result_image = result
        return result, total_object_pixels

    def _label_components(self, mask):
        """Connected component labeling (4-connectivity) on binary mask."""
        height = len(mask)
        width = len(mask[0]) if height > 0 else 0
        labels = [[0 for _ in range(width)] for _ in range(height)]
        current_label = 1
        objects = []

        for y in range(height):
            for x in range(width):
                if mask[y][x] == 1 and labels[y][x] == 0:
                    queue = [(y, x)]
                    labels[y][x] = current_label
                    min_x = max_x = x
                    min_y = max_y = y
                    sum_x = 0.0
                    sum_y = 0.0
                    pixel_count = 0
                    while queue:
                        cy, cx = queue.pop(0)
                        min_x = min(min_x, cx)
                        max_x = max(max_x, cx)
                        min_y = min(min_y, cy)
                        max_y = max(max_y, cy)
                        sum_x += cx
                        sum_y += cy
                        pixel_count += 1
                        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < height and 0 <= nx < width:
                                if mask[ny][nx] == 1 and labels[ny][nx] == 0:
                                    labels[ny][nx] = current_label
                                    queue.append((ny, nx))
                    centroid_x = sum_x / pixel_count
                    centroid_y = sum_y / pixel_count
                    objects.append({
                        'label': current_label,
                        'bbox': (min_x, min_y, max_x, max_y),
                        'centroid': (centroid_x, centroid_y),
                        'area': pixel_count
                    })
                    current_label += 1

        return objects