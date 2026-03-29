# color_filter.py
from PIL import Image
from modules.grayscale_converter import GrayscaleConverter

class ColorFilter:
    """Colorization filters that map grayscale intensity to colours."""

    @staticmethod
    def blue_ocean(gray_img):
        """Map grayscale to shades of blue (0 → dark blue, 255 → light cyan)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]  # grayscale value
                r = v // 2
                g = v
                b = 255
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def green_forest(gray_img):
        """Map grayscale to shades of green (0 → dark green, 255 → light green)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = v // 3
                g = v
                b = v // 3
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def red_sunset(gray_img):
        """Map grayscale to shades of red/orange (0 → dark red, 255 → bright orange)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = v
                g = v // 2
                b = 0
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def purple_night(gray_img):
        """Map grayscale to purple shades (0 → dark purple, 255 → lavender)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = v
                g = v // 2
                b = v
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def gold_metal(gray_img):
        """Map grayscale to golden tones (0 → dark gold, 255 → bright yellow)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = v
                g = int(v * 0.8)
                b = 0
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def pink_candy(gray_img):
        """Map grayscale to pink shades (0 → dark pink, 255 → light pink)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = 255
                g = v // 2
                b = v
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def cyan_water(gray_img):
        """Map grayscale to cyan/teal (0 → dark teal, 255 → light cyan)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = 0
                g = v
                b = v
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def autumn_leaves(gray_img):
        """Map grayscale to autumn colours (0 → brown, 255 → orange)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = v
                g = int(v * 0.5)
                b = 0
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def neon_glow(gray_img):
        """Map grayscale to high‑saturation neon colours (0 → magenta, 255 → cyan)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = (v * 2) % 256
                g = (v * 3) % 256
                b = (v * 5) % 256
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def grayscale_to_rgb(gray_img):
        """Convert grayscale to RGB (no change, but included for completeness)."""
        converter = GrayscaleConverter()
        return converter.convert_to_grayscale(gray_img)

    @staticmethod
    def heatmap(gray_img):
        """Map grayscale to thermal imaging colours (blue → green → red)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                if v < 85:
                    r = 0
                    g = int(v * 3)
                    b = 255 - int(v * 3)
                elif v < 170:
                    r = int((v - 85) * 3)
                    g = 255 - int((v - 85) * 3)
                    b = 0
                else:
                    r = 255
                    g = int((v - 170) * 3)
                    b = 0
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def rainbow(gray_img):
        """Map grayscale to full rainbow colours (ROYGBIV)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                hue = (v / 255.0) * 360
                c = 1.0
                x_val = c * (1 - abs((hue / 60) % 2 - 1))
                if hue < 60:
                    r, g, b = c, x_val, 0
                elif hue < 120:
                    r, g, b = x_val, c, 0
                elif hue < 180:
                    r, g, b = 0, c, x_val
                elif hue < 240:
                    r, g, b = 0, x_val, c
                elif hue < 300:
                    r, g, b = x_val, 0, c
                else:
                    r, g, b = c, 0, x_val
                res[x, y] = (int(r * 255), int(g * 255), int(b * 255))
        return result

    @staticmethod
    def vintage_paper(gray_img):
        """Map grayscale to sepia with a paper‑like fade."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = min(255, int(v * 1.2))
                g = min(255, int(v * 1.0))
                b = min(255, int(v * 0.8))
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def electric_blue(gray_img):
        """Map grayscale to electric blue tones (high‑contrast blue)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = v // 4
                g = v // 2
                b = v
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def sunset_gradient(gray_img):
        """Map grayscale to a sunset gradient (dark red → orange → yellow)."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                if v < 128:
                    r = v
                    g = v // 2
                    b = 0
                else:
                    r = 255
                    g = int((v - 128) * 2)
                    b = 0
                res[x, y] = (r, g, b)
        return result

    @staticmethod
    def forest_canopy(gray_img):
        """Map grayscale to deep forest greens and browns."""
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        w, h = gray_rgb.size
        pixels = gray_rgb.load()
        result = Image.new('RGB', (w, h))
        res = result.load()
        for y in range(h):
            for x in range(w):
                v = pixels[x, y][0]
                r = int(v * 0.3)
                g = v
                b = int(v * 0.2)
                res[x, y] = (r, g, b)
        return result