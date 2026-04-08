from modules.pixel_processor import process_pixels, get_image_info
from modules.grayscale_converter import GrayscaleConverter

class ThresholdConverter:
    def __init__(self):
        self.thresholded_image = None
        self.threshold_type = "single"  # "single", "range", "adaptive"
        self.t = 128
        self.t1 = 0
        self.t2 = 255
        self.block_size = 11
        self.c = 2

    def apply_single_threshold(self, pil_image, t=128):
        """Pixels >= t become white (255), else black (0)."""
        if pil_image is None:
            return None
        converter = GrayscaleConverter()
        gray_img = converter.convert_to_grayscale(pil_image)

        def threshold_transform(x, y, pixel):
            gray_val = pixel[0]
            return (255, 255, 255) if gray_val >= t else (0, 0, 0)

        self.thresholded_image = process_pixels(gray_img, threshold_transform, output_mode='RGB')
        self.threshold_type = "single"
        self.t = t
        return self.thresholded_image

    def apply_range_threshold(self, pil_image, t1=0, t2=255):
        """Pixels in [t1, t2] become white, else black."""
        if pil_image is None:
            return None
        converter = GrayscaleConverter()
        gray_img = converter.convert_to_grayscale(pil_image)

        def threshold_transform(x, y, pixel):
            gray_val = pixel[0]
            return (255, 255, 255) if t1 <= gray_val <= t2 else (0, 0, 0)

        self.thresholded_image = process_pixels(gray_img, threshold_transform, output_mode='RGB')
        self.threshold_type = "range"
        self.t1 = t1
        self.t2 = t2
        return self.thresholded_image

    def apply_adaptive_threshold(self, pil_image, block_size=11, c=2, method='mean'):
        """
        Adaptive thresholding: local threshold = mean of block - c.
        For each pixel, compute mean intensity of block_size x block_size neighborhood,
        then threshold: pixel = white if intensity >= (mean - c) else black.
        Uses manual loops (no OpenCV).
        """
        if pil_image is None:
            return None
        converter = GrayscaleConverter()
        gray_img = converter.convert_to_grayscale(pil_image)  # RGB with equal channels
        width, height, _, _, _ = get_image_info(gray_img)

        # Convert to 2D list of grayscale intensities (0-255) for faster access
        src_pixels = gray_img.load()
        intensity = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                intensity[y][x] = src_pixels[x, y][0]

        # Prepare result array
        result_intensity = [[0 for _ in range(width)] for _ in range(height)]

        half = block_size // 2
        for y in range(height):
            for x in range(width):
                # Determine block boundaries
                y_start = max(0, y - half)
                y_end = min(height, y + half + 1)
                x_start = max(0, x - half)
                x_end = min(width, x + half + 1)
                total = 0
                count = 0
                for iy in range(y_start, y_end):
                    for ix in range(x_start, x_end):
                        total += intensity[iy][ix]
                        count += 1
                mean = total / count
                local_threshold = mean - c
                result_intensity[y][x] = 255 if intensity[y][x] >= local_threshold else 0

        # Create output image from result_intensity
        from PIL import Image
        result_img = Image.new('RGB', (width, height))
        res_pixels = result_img.load()
        for y in range(height):
            for x in range(width):
                val = result_intensity[y][x]
                res_pixels[x, y] = (val, val, val)

        self.thresholded_image = result_img
        self.threshold_type = "adaptive"
        self.block_size = block_size
        self.c = c
        return self.thresholded_image

    # For backward compatibility, keep old method name
    def apply_threshold(self, pil_image, t1=None, t2=None, adaptive=False, block_size=11, c=2):
        if adaptive:
            return self.apply_adaptive_threshold(pil_image, block_size, c)
        elif t1 is not None and t2 is not None:
            return self.apply_range_threshold(pil_image, t1, t2)
        else:
            t = t1 if t1 is not None else 128
            return self.apply_single_threshold(pil_image, t)