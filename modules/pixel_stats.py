# pixel_stats.py
from PIL import Image  # used only for pixel access and size, not for statistics

class PixelStats:
    """Utility class for manual pixel statistics without PIL statistical methods."""

    @staticmethod
    def get_dimensions(image):
        """Return (width, height) of image."""
        return image.size

    @staticmethod
    def get_total_pixels(image):
        """Return total number of pixels."""
        w, h = image.size
        return w * h

    @staticmethod
    def get_grayscale_sum(image):
        """
        Compute sum of grayscale values of all pixels.
        If image is not grayscale, convert using luminosity method manually.
        Returns total sum and count.
        """
        # Ensure RGB mode for consistent access
        if image.mode not in ('RGB', 'RGBA'):
            img = image.convert('RGB')
        else:
            img = image
        pixels = img.load()
        w, h = img.size
        total = 0
        r_factor = 299
        g_factor = 587
        b_factor = 114
        for y in range(h):
            for x in range(w):
                pixel = pixels[x, y]
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                else:
                    r = g = b = pixel[0]
                gray = (r * r_factor + g * g_factor + b * b_factor) // 1000
                total += gray
        return total, w * h

    @staticmethod
    def get_histogram(image):
        """
        Return histogram of grayscale values as list of 256 ints.
        Uses manual luminosity conversion.
        """
        if image.mode not in ('RGB', 'RGBA'):
            img = image.convert('RGB')
        else:
            img = image
        pixels = img.load()
        w, h = img.size
        hist = [0] * 256
        r_factor = 299
        g_factor = 587
        b_factor = 114
        for y in range(h):
            for x in range(w):
                pixel = pixels[x, y]
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                else:
                    r = g = b = pixel[0]
                gray = (r * r_factor + g * g_factor + b * b_factor) // 1000
                hist[gray] += 1
        return hist

    @staticmethod
    def count_pixels_by_condition(image, condition_func):
        """
        Count pixels that satisfy condition_func(pixel).
        Pixel is passed as tuple (r,g,b) or (r,g,b,a).
        Returns count.
        """
        pixels = image.load()
        w, h = image.size
        count = 0
        for y in range(h):
            for x in range(w):
                pixel = pixels[x, y]
                if condition_func(pixel):
                    count += 1
        return count

    @staticmethod
    def get_grayscale_stats(image):
        """Return min, max, mean, std of grayscale values."""
        hist = PixelStats.get_histogram(image)
        total_pixels = sum(hist)
        if total_pixels == 0:
            return None

        # Mean
        sum_val = 0
        for i, cnt in enumerate(hist):
            sum_val += i * cnt
        mean = sum_val / total_pixels

        # Variance and std
        sum_sq = 0
        for i, cnt in enumerate(hist):
            sum_sq += (i - mean) ** 2 * cnt
        variance = sum_sq / total_pixels
        std = variance ** 0.5

        # Min and max (first and last non‑zero bins)
        min_val = next(i for i, cnt in enumerate(hist) if cnt > 0)
        max_val = next(i for i in range(255, -1, -1) if hist[i] > 0)

        return {
            'min': min_val,
            'max': max_val,
            'mean': mean,
            'std': std,
            'total_pixels': total_pixels
        }