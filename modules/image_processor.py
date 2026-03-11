import os
from PIL import Image
from modules.pixel_stats import PixelStats   # new import

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
    
    # New method that uses PixelStats (optional, to satisfy "call it")
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