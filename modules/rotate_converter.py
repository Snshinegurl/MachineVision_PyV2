from PIL import Image
import math

class ImageRotator:
    def __init__(self):
        self.rotated_image = None
        self.angle = 0

    def rotate_image(self, pil_image, angle):
        """
        Rotate a PIL image around its center by the given angle (degrees),
        keeping the same dimensions. Empty areas become black (RGB) or transparent (RGBA).
        """
        if not pil_image:
            return None

        # Ensure we work with RGB or RGBA
        original_mode = pil_image.mode
        if original_mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
            original_mode = 'RGB'

        rads = math.radians(angle)
        width, height = pil_image.size
        midx, midy = width // 2, height // 2

        # Create result image
        result = Image.new(original_mode, (width, height))
        src_pixels = pil_image.load()
        dst_pixels = result.load()

        # Inverse mapping – for each destination pixel find source pixel
        for y in range(height):
            for x in range(width):
                # Translate to centre coordinates
                dx = x - midx
                dy = y - midy

                # Inverse rotation
                src_x = dx * math.cos(rads) + dy * math.sin(rads) + midx
                src_y = -dx * math.sin(rads) + dy * math.cos(rads) + midy

                src_x_round = int(round(src_x))
                src_y_round = int(round(src_y))

                if 0 <= src_x_round < width and 0 <= src_y_round < height:
                    dst_pixels[x, y] = src_pixels[src_x_round, src_y_round]
                else:
                    # Fill empty area
                    if original_mode == 'RGBA':
                        dst_pixels[x, y] = (0, 0, 0, 0)
                    else:
                        dst_pixels[x, y] = (0, 0, 0)

        self.rotated_image = result
        self.angle = angle
        return result