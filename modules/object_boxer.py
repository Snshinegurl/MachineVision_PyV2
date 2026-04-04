from PIL import Image
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
        then draw bounding boxes manually and set background to grayscale.
        Returns (image, total_object_pixels).
        """

        # Step 1: Background removal
        bg_remover = BackgroundRemover()
        rgba_img = bg_remover.remove_background(pil_image, tolerance=30)
        if rgba_img is None:
            raise Exception("Background removal failed - cannot detect objects")

        width, height = rgba_img.size

        # Step 2: Create foreground mask
        fg_mask = [[0 for _ in range(width)] for _ in range(height)]
        pixels = rgba_img.load()

        for y in range(height):
            for x in range(width):
                if pixels[x, y][3] > 0:  # alpha channel
                    fg_mask[y][x] = 1

        # Step 3: Connected component labeling
        objects = self._label_components(fg_mask)

        total_object_pixels = sum(obj['area'] for obj in objects)
        self.object_area = total_object_pixels
        self.objects = objects

        # Step 4: Convert full image to grayscale
        converter = GrayscaleConverter()
        grayscale_full = converter.convert_to_grayscale(pil_image)

        if grayscale_full.mode != 'RGB':
            grayscale_full = grayscale_full.convert('RGB')

        result = grayscale_full.copy()
        result_pixels = result.load()

        # Step 5: Prepare original RGB
        if pil_image.mode != 'RGB':
            original_rgb = pil_image.convert('RGB')
        else:
            original_rgb = pil_image

        original_pixels = original_rgb.load()

        # Step 6: Restore foreground color
        for y in range(height):
            for x in range(width):
                if fg_mask[y][x] == 1:
                    result_pixels[x, y] = original_pixels[x, y]

        # Step 7: Draw bounding boxes manually
        for obj in objects:
            self._draw_box_manual(result, obj['bbox'], color=(255, 0, 0), thickness=2)

        self.result_image = result
        return result, total_object_pixels

    def _draw_box_manual(self, image, bbox, color=(255, 0, 0), thickness=2):
        """Draw rectangle manually using pixel manipulation."""
        x1, y1, x2, y2 = bbox
        pixels = image.load()
        width, height = image.size

        for t in range(thickness):
            # Top & Bottom borders
            for x in range(x1, x2 + 1):
                if 0 <= x < width:
                    if 0 <= y1 + t < height:
                        pixels[x, y1 + t] = color
                    if 0 <= y2 - t < height:
                        pixels[x, y2 - t] = color

            # Left & Right borders
            for y in range(y1, y2 + 1):
                if 0 <= y < height:
                    if 0 <= x1 + t < width:
                        pixels[x1 + t, y] = color
                    if 0 <= x2 - t < width:
                        pixels[x2 - t, y] = color

    def _label_components(self, mask):
        """Connected component labeling (4-connectivity)."""
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