# pixel_stats.py
from PIL import Image

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
    def get_rgb_histograms(image):
        """
        Return three histograms (r, g, b) as lists of 256 ints.
        If image has alpha, it is ignored.
        """
        # Ensure RGB mode
        if image.mode not in ('RGB', 'RGBA'):
            img = image.convert('RGB')
        else:
            img = image
        pixels = img.load()
        w, h = img.size
        r_hist = [0] * 256
        g_hist = [0] * 256
        b_hist = [0] * 256
        for y in range(h):
            for x in range(w):
                pixel = pixels[x, y]
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                else:
                    r = g = b = pixel[0]
                r_hist[r] += 1
                g_hist[g] += 1
                b_hist[b] += 1
        return r_hist, g_hist, b_hist

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

        sum_val = 0
        for i, cnt in enumerate(hist):
            sum_val += i * cnt
        mean = sum_val / total_pixels

        sum_sq = 0
        for i, cnt in enumerate(hist):
            sum_sq += (i - mean) ** 2 * cnt
        variance = sum_sq / total_pixels
        std = variance ** 0.5

        min_val = next(i for i, cnt in enumerate(hist) if cnt > 0)
        max_val = next(i for i in range(255, -1, -1) if hist[i] > 0)

        return {
            'min': min_val,
            'max': max_val,
            'mean': mean,
            'std': std,
            'total_pixels': total_pixels
        }
    
    @staticmethod
    def get_centroid(image):
        """
        Compute the centroid (center of mass) of the image based on pixel intensities.
        For RGB images, convert to grayscale first.
        Returns (cx, cy) as floats, or None if total intensity is zero.
        """
        if image.mode not in ('L', 'RGB', 'RGBA'):
            image = image.convert('L')
        
        # Convert to grayscale if needed
        if image.mode != 'L':
            from modules.grayscale_converter import GrayscaleConverter
            converter = GrayscaleConverter()
            gray = converter.convert_to_grayscale(image)
        else:
            gray = image
        
        pixels = gray.load()
        w, h = gray.size
        
        total_intensity = 0
        sum_x = 0.0
        sum_y = 0.0
        
        for y in range(h):
            for x in range(w):
                intensity = pixels[x, y][0] if isinstance(pixels[x, y], tuple) else pixels[x, y]
                total_intensity += intensity
                sum_x += x * intensity
                sum_y += y * intensity
        
        if total_intensity == 0:
            return None
        
        cx = sum_x / total_intensity
        cy = sum_y / total_intensity
        return (cx, cy)