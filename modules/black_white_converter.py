from PIL import Image
from modules.grayscale_converter import GrayscaleConverter
from modules.background_remover import BackgroundRemover
from modules.pixel_stats import PixelStats
from modules.pixel_processor import process_pixels

class BlackWhiteConverter:
    def __init__(self):
        self.black_white_image = None
        self.width = 0
        self.height = 0
        self.grayscale_converter = GrayscaleConverter()
        self.background_remover = BackgroundRemover()
        self.threshold = 128

    def convert_to_black_white(self, pil_image, threshold=None, method='manual'):
        if not pil_image:
            return None

        # First get grayscale image (already uses process_pixels)
        grayscale_image = self.grayscale_converter.convert_to_grayscale(pil_image)
        if not grayscale_image:
            return None

        self.width, self.height = grayscale_image.size

        if threshold is not None:
            self.threshold = threshold
        elif method == 'otsu':
            self.threshold = self._calculate_otsu_threshold(grayscale_image)
        else:
            self.threshold = 128

        # Pixel transform for thresholding
        def threshold_transform(x, y, pixel):
            # pixel is (gray, gray, gray)
            gray_value = pixel[0]
            bw_value = 0 if gray_value < self.threshold else 255
            return (bw_value, bw_value, bw_value)

        self.black_white_image = process_pixels(grayscale_image, threshold_transform, output_mode='RGB')
        return self.black_white_image

    def _calculate_otsu_threshold(self, grayscale_image):
        """Use PixelStats histogram for Otsu's method (still manual loops)."""
        hist = PixelStats.get_histogram(grayscale_image)
        total_pixels = sum(hist)
        if total_pixels == 0:
            return 128

        sum_total = 0
        for i in range(256):
            sum_total += i * hist[i]

        sum_back = 0
        weight_back = 0
        variance_max = 0
        optimal_threshold = 128

        for threshold in range(256):
            weight_back += hist[threshold]
            if weight_back == 0:
                continue
            weight_fore = total_pixels - weight_back
            if weight_fore == 0:
                break
            sum_back += threshold * hist[threshold]
            mean_back = sum_back / weight_back
            mean_fore = (sum_total - sum_back) / weight_fore
            variance_between = weight_back * weight_fore * (mean_back - mean_fore) ** 2
            if variance_between > variance_max:
                variance_max = variance_between
                optimal_threshold = threshold

        return optimal_threshold

    # Other methods (convert_with_multiple_thresholds, remove_background, get_stats, etc.)
    # remain unchanged. They are included below for completeness.

    def convert_with_multiple_thresholds(self, pil_image, low_threshold=85, high_threshold=170):
        if not pil_image:
            return None

        grayscale_image = self.grayscale_converter.convert_manual_loop(pil_image)
        if not grayscale_image:
            return None

        self.width, self.height = grayscale_image.size
        three_level_image = Image.new('RGB', (self.width, self.height))
        source_pixels = grayscale_image.load()
        target_pixels = three_level_image.load()

        for y in range(self.height):
            for x in range(self.width):
                gray_value = source_pixels[x, y][0]
                if gray_value < low_threshold:
                    level_value = 0
                elif gray_value < high_threshold:
                    level_value = 128
                else:
                    level_value = 255
                target_pixels[x, y] = (level_value, level_value, level_value)

        self.black_white_image = three_level_image
        return self.black_white_image

    def remove_background(self, pil_image, method='auto', tolerance=30, bg_color=None):
        if method == 'simple':
            return self.background_remover.remove_background_simple(pil_image, bg_color, tolerance)
        else:
            return self.background_remover.remove_background(pil_image, tolerance)

    def get_background_removal_stats(self):
        return self.background_remover.get_stats()

    def get_threshold_info(self):
        return {
            'threshold': self.threshold,
            'threshold_description': self._get_threshold_description()
        }

    def _get_threshold_description(self):
        if self.threshold < 85:
            return "Low threshold (dark images)"
        elif self.threshold < 128:
            return "Medium-low threshold"
        elif self.threshold < 170:
            return "Medium threshold"
        elif self.threshold < 200:
            return "Medium-high threshold"
        else:
            return "High threshold (bright images)"

    def get_black_white_stats(self):
        if not self.black_white_image:
            return None

        black_count = PixelStats.count_pixels_by_condition(
            self.black_white_image,
            lambda p: p[0] < 128
        )
        white_count = PixelStats.count_pixels_by_condition(
            self.black_white_image,
            lambda p: p[0] >= 128
        )
        total_pixels = self.width * self.height

        return {
            'black_pixels': black_count,
            'white_pixels': white_count,
            'black_percentage': (black_count / total_pixels) * 100 if total_pixels > 0 else 0,
            'white_percentage': (white_count / total_pixels) * 100 if total_pixels > 0 else 0,
            'threshold_used': self.threshold,
            'threshold_method': 'Otsu' if self.threshold != 128 else 'Fixed',
            'width': self.width,
            'height': self.height,
            'total_pixels': total_pixels
        }

    def visualize_threshold(self, pil_image):
        if not pil_image:
            return None

        grayscale_image = self.grayscale_converter.convert_manual_loop(pil_image)
        if not grayscale_image:
            return None

        hist = PixelStats.get_histogram(grayscale_image)

        from PIL import ImageDraw
        viz_width = 512
        viz_height = 256
        viz_image = Image.new('RGB', (viz_width, viz_height), color='white')
        draw = ImageDraw.Draw(viz_image)

        max_hist = max(hist) if hist else 1
        bar_width = viz_width // 256
        for i in range(256):
            bar_height = (hist[i] / max_hist) * (viz_height - 20)
            x1 = i * bar_width
            x2 = (i + 1) * bar_width
            y1 = viz_height - bar_height
            y2 = viz_height
            draw.rectangle([x1, y1, x2, y2], fill='blue')

        threshold_x = self.threshold * bar_width
        draw.line([threshold_x, 0, threshold_x, viz_height], fill='red', width=2)
        draw.text((10, 10), f"Threshold: {self.threshold}", fill='black')
        draw.text((10, 30), f"Method: {'Otsu' if self.threshold != 128 else 'Fixed'}", fill='black')

        return viz_image