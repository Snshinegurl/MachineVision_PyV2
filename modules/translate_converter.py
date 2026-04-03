from PIL import Image

class ImageTranslator:
    def __init__(self):
        self.translated_image = None
        self.dx = 0
        self.dy = 0

    def translate_image(self, pil_image, dx, dy):
        """
        Translate (shift) the image by dx (horizontal) and dy (vertical).
        Positive dx = shift right, positive dy = shift down.
        Empty areas become black (RGB) or transparent (RGBA).
        Uses manual pixel loops – no PIL built‑in shift.
        """
        if not pil_image:
            return None

        original_mode = pil_image.mode
        if original_mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
            original_mode = 'RGB'

        width, height = pil_image.size
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