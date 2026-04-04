from PIL import Image
from modules.grayscale_converter import GrayscaleConverter
from modules.pixel_processor import process_pixels

class ColorFilter:
    """Colorization filters that map grayscale intensity to colours."""

    @staticmethod
    def _apply_color_map(gray_img, color_func):
        """
        Helper: convert grayscale image (RGB mode, three equal channels) to color using process_pixels.
        color_func takes a grayscale value (0-255) and returns (r, g, b) tuple.
        """
        # gray_img is RGB but all channels equal; we take the first channel as intensity
        def transform(x, y, pixel):
            v = pixel[0]  # grayscale intensity
            return color_func(v)
        return process_pixels(gray_img, transform, output_mode='RGB')

    @staticmethod
    def blue_ocean(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (v // 2, v, 255))

    @staticmethod
    def green_forest(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (v // 3, v, v // 3))

    @staticmethod
    def red_sunset(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (v, v // 2, 0))

    @staticmethod
    def purple_night(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (v, v // 2, v))

    @staticmethod
    def gold_metal(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (v, int(v * 0.8), 0))

    @staticmethod
    def pink_candy(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (255, v // 2, v))

    @staticmethod
    def cyan_water(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (0, v, v))

    @staticmethod
    def autumn_leaves(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (v, int(v * 0.5), 0))

    @staticmethod
    def neon_glow(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: ((v * 2) % 256, (v * 3) % 256, (v * 5) % 256))

    @staticmethod
    def grayscale_to_rgb(gray_img):
        converter = GrayscaleConverter()
        return converter.convert_to_grayscale(gray_img)

    @staticmethod
    def heatmap(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        def heatmap_func(v):
            if v < 85:
                return (0, v * 3, 255 - v * 3)
            elif v < 170:
                return ((v - 85) * 3, 255 - (v - 85) * 3, 0)
            else:
                return (255, (v - 170) * 3, 0)
        return ColorFilter._apply_color_map(gray_rgb, heatmap_func)

    @staticmethod
    def rainbow(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        def rainbow_func(v):
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
            return (int(r * 255), int(g * 255), int(b * 255))
        return ColorFilter._apply_color_map(gray_rgb, rainbow_func)

    @staticmethod
    def vintage_paper(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (min(255, int(v * 1.2)), min(255, int(v * 1.0)), min(255, int(v * 0.8))))

    @staticmethod
    def electric_blue(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (v // 4, v // 2, v))

    @staticmethod
    def sunset_gradient(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        def sunset_func(v):
            if v < 128:
                return (v, v // 2, 0)
            else:
                return (255, int((v - 128) * 2), 0)
        return ColorFilter._apply_color_map(gray_rgb, sunset_func)

    @staticmethod
    def forest_canopy(gray_img):
        converter = GrayscaleConverter()
        gray_rgb = converter.convert_to_grayscale(gray_img)
        return ColorFilter._apply_color_map(gray_rgb, lambda v: (int(v * 0.3), v, int(v * 0.2)))