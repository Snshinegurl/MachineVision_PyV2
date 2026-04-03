from PIL import Image, ImageDraw
from modules.grayscale_converter import GrayscaleConverter

class ObjectBoxer:
    def __init__(self):
        self.result_image = None
        self.object_area = 0          # NEW: store total object pixels
        self.threshold = 128

    def box_objects(self, pil_image, threshold=128):
        """
        Detect objects (connected components), draw bounding boxes,
        set background to grayscale, and return (image, object_area).
        """
        # Convert to grayscale using our module if needed
        if pil_image.mode != 'L':
            converter = GrayscaleConverter()
            gray_img = converter.convert_to_grayscale(pil_image)
        else:
            gray_img = pil_image

        self.threshold = threshold
        width, height = gray_img.size

        # 1. Binary mask: 1 for foreground, 0 for background
        pixels = gray_img.load()
        mask = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                val = pixels[x, y][0]
                mask[y][x] = 1 if val >= threshold else 0

        # 2. Connected component labeling (4‑connectivity)
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

        # 3. Compute bounding boxes and count total object pixels
        boxes = {}
        total_object_pixels = 0
        for y in range(height):
            for x in range(width):
                label = labels[y][x]
                if label > 0:
                    total_object_pixels += 1
                    if label not in boxes:
                        boxes[label] = {'min_x': x, 'max_x': x, 'min_y': y, 'max_y': y}
                    else:
                        boxes[label]['min_x'] = min(boxes[label]['min_x'], x)
                        boxes[label]['max_x'] = max(boxes[label]['max_x'], x)
                        boxes[label]['min_y'] = min(boxes[label]['min_y'], y)
                        boxes[label]['max_y'] = max(boxes[label]['max_y'], y)

        self.object_area = total_object_pixels

        # 4. Build result image: keep original colours inside objects,
        #    background becomes grayscale (using the same luminosity formula)
        if pil_image.mode != 'RGB':
            result = pil_image.convert('RGB')
        else:
            result = pil_image.copy()
        result_pixels = result.load()

        for y in range(height):
            for x in range(width):
                if labels[y][x] == 0:  # background
                    orig = result_pixels[x, y]
                    gray = int(0.299 * orig[0] + 0.587 * orig[1] + 0.114 * orig[2])
                    result_pixels[x, y] = (gray, gray, gray)

        # 5. Draw red bounding boxes
        draw = ImageDraw.Draw(result)
        for label, bbox in boxes.items():
            draw.rectangle([bbox['min_x'], bbox['min_y'],
                            bbox['max_x'], bbox['max_y']],
                           outline='red', width=2)

        self.result_image = result
        return result, total_object_pixels   # NEW: return area as well