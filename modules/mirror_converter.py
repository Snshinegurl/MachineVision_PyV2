from modules.pixel_processor import process_pixels

class ImageMirror:
    def __init__(self):
        self.mirrored_image = None
        self.mirror_type = "horizontal"

    def mirror_horizontal(self, pil_image):
        """Mirror horizontally using manual pixel mapping."""
        def h_mirror_transform(x, y, pixel):
            pass
        width, height = pil_image.size
        # Convert PIL to list of lists of tuples
        pixels = pil_image.load()
        img_list = [[pixels[x, y] for x in range(width)] for y in range(height)]
        # Apply horizontal mirror (reverse each row)
        mirrored_list = [row[::-1] for row in img_list]
        # Create new PIL image from list
        from PIL import Image
        result = Image.new('RGB', (width, height))
        res_pixels = result.load()
        for y in range(height):
            for x in range(width):
                res_pixels[x, y] = mirrored_list[y][x]
        self.mirrored_image = result
        return result

    def mirror_vertical(self, pil_image):
        """Mirror vertically using manual pixel mapping."""
        width, height = pil_image.size
        pixels = pil_image.load()
        img_list = [[pixels[x, y] for x in range(width)] for y in range(height)]
        # Reverse rows
        mirrored_list = img_list[::-1]
        from PIL import Image
        result = Image.new('RGB', (width, height))
        res_pixels = result.load()
        for y in range(height):
            for x in range(width):
                res_pixels[x, y] = mirrored_list[y][x]
        self.mirrored_image = result
        return result

    def mirror(self, pil_image, mirror_type='horizontal'):
        self.mirror_type = mirror_type
        if mirror_type == 'horizontal':
            return self.mirror_horizontal(pil_image)
        else:
            return self.mirror_vertical(pil_image)