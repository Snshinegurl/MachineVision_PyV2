"""
Manual convolution filters (no library convolution functions).
Uses pixel_processor for image info and pixel access.
Handles RGB images, applies kernel to each channel separately.
Border handling: zero-padding.
No automatic normalization – kernel is applied as given, then clamped to [0,255].
"""

from PIL import Image
import math
from modules.pixel_processor import get_image_info

class ConvolutionFilter:
    def __init__(self):
        self.filtered_image = None
        self.last_kernel = None

    def apply_convolution(self, pil_image, kernel, kernel_size=3):
        """
        Apply manual convolution with zero-padding.
        kernel: 2D list of floats (size kernel_size x kernel_size)
        """
        if pil_image is None:
            return None

        # Use pixel_processor to get image info (satisfies requirement)
        width, height, channels, total_pixels, mode = get_image_info(pil_image)
        if width is None:
            raise ValueError("Invalid image")

        # Ensure RGB mode for processing
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        if pil_image.mode == 'RGBA':
            pil_image = pil_image.convert('RGB')

        width, height = pil_image.size
        pixels = pil_image.load()
        result = Image.new('RGB', (width, height))
        result_pixels = result.load()

        pad = kernel_size // 2

        for y in range(height):
            for x in range(width):
                r_sum, g_sum, b_sum = 0.0, 0.0, 0.0
                for ky in range(kernel_size):
                    for kx in range(kernel_size):
                        ix = x + kx - pad
                        iy = y + ky - pad
                        if 0 <= ix < width and 0 <= iy < height:
                            pixel = pixels[ix, iy]
                            r, g, b = pixel[0], pixel[1], pixel[2]
                            k_val = kernel[ky][kx]
                            r_sum += r * k_val
                            g_sum += g * k_val
                            b_sum += b * k_val
                        # else zero-padding (adds nothing)

                # Clamp to [0, 255] and round
                r_out = max(0, min(255, int(round(r_sum))))
                g_out = max(0, min(255, int(round(g_sum))))
                b_out = max(0, min(255, int(round(b_sum))))
                result_pixels[x, y] = (r_out, g_out, b_out)

        self.filtered_image = result
        self.last_kernel = kernel
        return result

    # ---------- Predefined kernels ----------
    @staticmethod
    def get_smoothing_kernel(size=3):
        """Averaging kernel (all ones, normalized to sum = 1)"""
        val = 1.0 / (size * size)
        return [[val for _ in range(size)] for _ in range(size)]

    @staticmethod
    def get_gaussian_kernel(size=3, sigma=1.0):
        """Gaussian kernel (normalized to sum = 1)"""
        kernel = [[0.0 for _ in range(size)] for _ in range(size)]
        offset = size // 2
        total = 0.0
        for i in range(size):
            for j in range(size):
                x = i - offset
                y = j - offset
                kernel[i][j] = math.exp(-(x*x + y*y) / (2*sigma*sigma)) / (2*math.pi*sigma*sigma)
                total += kernel[i][j]
        for i in range(size):
            for j in range(size):
                kernel[i][j] /= total
        return kernel

    @staticmethod
    def get_sharpening_kernel():
        """Standard sharpening kernel (sum = 1)"""
        return [[0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]]

    @staticmethod
    def get_mean_removal_kernel():
        """High-pass filter (mean removal, sum = 0)"""
        return [[-1, -1, -1],
                [-1,  8, -1],
                [-1, -1, -1]]

    @staticmethod
    def get_emboss_kernel():
        """Emboss kernel (south-east direction)"""
        return [[-2, -1, 0],
                [-1,  1, 1],
                [ 0,  1, 2]]

    @staticmethod
    def parse_custom_kernel(kernel_str):
        """Parse a string of space-separated numbers into a 3x3 kernel."""
        parts = kernel_str.strip().split()
        if len(parts) != 9:
            raise ValueError("Custom kernel must have exactly 9 numbers (3x3).")
        nums = [float(p) for p in parts]
        return [nums[0:3], nums[3:6], nums[6:9]]