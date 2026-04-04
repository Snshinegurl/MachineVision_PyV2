from PIL import Image
import math
from modules.pixel_processor import process_pixels, get_image_info

class ImageRotator:
    def __init__(self):
        self.rotated_image = None
        self.angle = 0

    def rotate_image(self, pil_image, angle):
        """
        Rotate a PIL image around its center by the given angle (degrees),
        keeping the same dimensions. Empty areas become black (RGB) or transparent (RGBA).
        Uses pixel_processor to access all source pixels.
        """
        if not pil_image:
            return None

        # Ensure we work with RGB or RGBA
        original_mode = pil_image.mode
        if original_mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
            original_mode = 'RGB'

        # Get image dimensions via pixel_processor
        width, height, _, _, _ = get_image_info(pil_image)
        rads = math.radians(angle)
        midx, midy = width // 2, height // 2

        # ---- Use process_pixels to extract all source pixels into a 2D list ----
        src_pixels_2d = []

        def collect_pixel(x, y, pixel):
            # This callback is called for each pixel in order (row by row)
            if y >= len(src_pixels_2d):
                src_pixels_2d.append([])
            src_pixels_2d[y].append(pixel)
            return pixel  # dummy return, we don't use the output image

        # Run process_pixels (it iterates over all pixels and calls collect_pixel)
        process_pixels(pil_image, collect_pixel, output_mode=original_mode)

        # ---- Create output image and fill using inverse mapping ----
        result = Image.new(original_mode, (width, height))
        dst_pixels = result.load()  # writing directly is still needed

        for y in range(height):
            for x in range(width):
                dx = x - midx
                dy = y - midy

                # Inverse rotation
                src_x = dx * math.cos(rads) + dy * math.sin(rads) + midx
                src_y = -dx * math.sin(rads) + dy * math.cos(rads) + midy

                src_x_round = int(round(src_x))
                src_y_round = int(round(src_y))

                if 0 <= src_x_round < width and 0 <= src_y_round < height:
                    dst_pixels[x, y] = src_pixels_2d[src_y_round][src_x_round]
                else:
                    # Fill empty area
                    if original_mode == 'RGBA':
                        dst_pixels[x, y] = (0, 0, 0, 0)
                    else:
                        dst_pixels[x, y] = (0, 0, 0)

        self.rotated_image = result
        self.angle = angle
        return result