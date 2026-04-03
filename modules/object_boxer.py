from PIL import Image, ImageDraw
from modules.grayscale_converter import GrayscaleConverter

class ObjectBoxer:
    def __init__(self):
        self.result_image = None
        self.threshold = 128

    def box_objects(self, pil_image, threshold=128):
        """
        Detect objects (connected components) in a grayscale image using a threshold,
        draw bounding boxes around them, and set background to grayscale.
        Returns an RGB image with boxes drawn and background grayed out.
        """
        # Convert to grayscale using our module if needed
        if pil_image.mode != 'L':
            converter = GrayscaleConverter()
            gray_img = converter.convert_to_grayscale(pil_image)
        else:
            gray_img = pil_image

        self.threshold = threshold
        width, height = gray_img.size

        # 1. Create binary mask: 1 for foreground (object), 0 for background
        pixels = gray_img.load()
        mask = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                val = pixels[x, y][0]  # grayscale value
                mask[y][x] = 1 if val >= threshold else 0

        # 2. Connected component labeling (4-connectivity) using BFS
        labels = [[0 for _ in range(width)] for _ in range(height)]
        current_label = 1
        for y in range(height):
            for x in range(width):
                if mask[y][x] == 1 and labels[y][x] == 0:
                    queue = [(y, x)]
                    labels[y][x] = current_label
                    while queue:
                        cy, cx = queue.pop(0)
                        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < height and 0 <= nx < width:
                                if mask[ny][nx] == 1 and labels[ny][nx] == 0:
                                    labels[ny][nx] = current_label
                                    queue.append((ny, nx))
                    current_label += 1

        # 3. Compute bounding boxes for each label
        boxes = {}
        for y in range(height):
            for x in range(width):
                label = labels[y][x]
                if label > 0:
                    if label not in boxes:
                        boxes[label] = {'min_x': x, 'max_x': x, 'min_y': y, 'max_y': y}
                    else:
                        boxes[label]['min_x'] = min(boxes[label]['min_x'], x)
                        boxes[label]['max_x'] = max(boxes[label]['max_x'], x)
                        boxes[label]['min_y'] = min(boxes[label]['min_y'], y)
                        boxes[label]['max_y'] = max(boxes[label]['max_y'], y)

        # 4. Create result image: start with a grayscale version of the original
        #    Then replace background with grayscale (already grayscale), but we need RGB
        #    Actually, we want original colors inside boxes, grayscale outside.
        #    So we'll convert the original image to RGB (keeping colors), then
        #    for background pixels we compute grayscale value using the converter.
        if pil_image.mode != 'RGB':
            result = pil_image.convert('RGB')
        else:
            result = pil_image.copy()
        result_pixels = result.load()

        # Use GrayscaleConverter to get the grayscale value for each background pixel
        converter = GrayscaleConverter()
        # Pre‑compute grayscale version for speed (optional)
        # For each background pixel, compute grayscale once.
        for y in range(height):
            for x in range(width):
                if labels[y][x] == 0:  # background
                    # Get original pixel (RGB)
                    orig_pixel = result_pixels[x, y]
                    # Compute grayscale using the same method as converter
                    gray_val = int(0.299 * orig_pixel[0] + 0.587 * orig_pixel[1] + 0.114 * orig_pixel[2])
                    result_pixels[x, y] = (gray_val, gray_val, gray_val)

        # 5. Draw bounding boxes (red outline)
        draw = ImageDraw.Draw(result)
        for label, bbox in boxes.items():
            x1 = bbox['min_x']
            y1 = bbox['min_y']
            x2 = bbox['max_x']
            y2 = bbox['max_y']
            draw.rectangle([x1, y1, x2, y2], outline='red', width=2)

        self.result_image = result
        return result