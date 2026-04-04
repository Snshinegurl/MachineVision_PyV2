from PIL import Image
from modules.pixel_stats import PixelStats
from modules.pixel_processor import process_pixels

class GrayscaleConverter:
    def __init__(self):
        self.grayscale_image = None
        self.width = 0
        self.height = 0

    def convert_to_grayscale(self, pil_image):
        """Convert PIL Image to grayscale using process_pixels."""
        if not pil_image:
            return None

        # Ensure RGB mode for consistent pixel access
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')

        self.width, self.height = pil_image.size

        def grayscale_transform(x, y, pixel):
            # pixel is a tuple of length 3 or 4; take first three
            if len(pixel) >= 3:
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                r = g = b = pixel[0]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray = max(0, min(255, gray))
            return (gray, gray, gray)

        self.grayscale_image = process_pixels(pil_image, grayscale_transform, output_mode='RGB')
        return self.grayscale_image

    def get_grayscale_stats(self):
        """Get statistics using PixelStats utility."""
        if not self.grayscale_image:
            return None

        stats = PixelStats.get_grayscale_stats(self.grayscale_image)
        if stats:
            stats['width'] = self.width
            stats['height'] = self.height
        return stats

    def get_histogram(self):
        """Get histogram using PixelStats."""
        if not self.grayscale_image:
            return None
        return PixelStats.get_histogram(self.grayscale_image)

    def get_brightness_info(self):
        """Get brightness classification based on mean value."""
        stats = self.get_grayscale_stats()
        if not stats:
            return None

        mean_val = stats['mean']
        if mean_val < 85:
            category = "Dark"
            description = "Image is predominantly dark"
        elif mean_val < 170:
            category = "Medium"
            description = "Image has balanced brightness"
        else:
            category = "Bright"
            description = "Image is predominantly bright"

        return {
            'mean_brightness': mean_val,
            'category': category,
            'description': description,
            'contrast': stats['std']
        }