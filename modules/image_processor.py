import os
from PIL import Image
from modules.pixel_stats import PixelStats

class ImageProcessor:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.total_pixels = 0
        self.pixel_data = None
        self.image_name = ""
        self.image_path = ""
        self.format = ""
        self.pil_image = None
        self.file_size = 0

    def load_image(self, image_path):
        self.image_path = image_path
        self.image_name = os.path.basename(image_path)

        try:
            self.pil_image = Image.open(image_path)
            self.width, self.height = self.pil_image.size
            self.format = self.pil_image.format
            self.total_pixels = self.width * self.height
            self.file_size = os.path.getsize(image_path)

            return {
                'name': self.image_name,
                'path': image_path,
                'width': self.width,
                'height': self.height,
                'total_pixels': self.total_pixels,
                'format': self.format,
                'file_size': self.file_size,
                'pil_image': self.pil_image,
                'supported': True
            }
        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")

    def get_image_info(self):
        if not self.pil_image:
            return None
        return {
            'name': self.image_name,
            'width': self.width,
            'height': self.height,
            'total_pixels': self.total_pixels,
            'format': self.format,
            'file_size': self.file_size
        }

    def get_pixel_summary(self):
        """Return basic pixel statistics using PixelStats."""
        if not self.pil_image:
            return None
        total_sum, count = PixelStats.get_grayscale_sum(self.pil_image)
        return {
            'total_pixels': count,
            'grayscale_sum': total_sum,
            'mean_grayscale': total_sum / count if count else 0
        }

    # NEW: Compute object area based on filter type
    def compute_object_area(self, pil_image, filter_type):
        """
        Return number of foreground pixels (object area).
        For background removal (RGBA): count non‑transparent pixels (alpha > 0).
        For Black & White (RGB binary): count white pixels (value 255).
        For other filters: return total image pixels.
        """
        if pil_image is None:
            return 0

        width, height = pil_image.size

        if filter_type == "background_removal":
            # Expect RGBA image
            if pil_image.mode == 'RGBA':
                pixels = pil_image.load()
                count = 0
                for y in range(height):
                    for x in range(width):
                        if pixels[x, y][3] > 0:
                            count += 1
                return count
            else:
                # Fallback: treat entire image as object
                return width * height

        elif filter_type == "custom_bw":
            # Expect RGB image with values 0 or 255
            if pil_image.mode == 'RGB':
                pixels = pil_image.load()
                count = 0
                for y in range(height):
                    for x in range(width):
                        # Any channel is enough (they are all the same)
                        if pixels[x, y][0] == 255:
                            count += 1
                return count
            else:
                return width * height

        else:
            # For all other filters (grayscale, color, rotate, mirror) return total pixels
            return width * height