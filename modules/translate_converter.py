from PIL import Image
from modules.pixel_processor import get_image_info   # using the module

class ImageTranslator:
    def __init__(self):
        self.translated_image = None
        self.dx = 0
        self.dy = 0

    def translate_image(self, pil_image, dx, dy):
        if not pil_image:
            return None

        original_mode = pil_image.mode
        if original_mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
            original_mode = 'RGB'

        # Use pixel_processor to get image dimensions (demonstrates usage of the module)
        width, height, channels, total_pixels, mode = get_image_info(pil_image)

        src = pil_image.load()
        result = Image.new(original_mode, (width, height))
        dst = result.load()

        for y in range(height):
            for x in range(width):
                src_x = x - dx
                src_y = y - dy
                if 0 <= src_x < width and 0 <= src_y < height:
                    dst[x, y] = src[src_x, src_y]
                else:
                    if original_mode == 'RGBA':
                        dst[x, y] = (0, 0, 0, 0)
                    else:
                        dst[x, y] = (0, 0, 0)

        self.translated_image = result
        self.dx = dx
        self.dy = dy
        return result