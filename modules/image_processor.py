import os
from PIL import Image

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
        """
        Load an image from file path
        Returns: dict with image information
        """
        self.image_path = image_path
        self.image_name = os.path.basename(image_path)
        
        try:
            # Load PIL image
            self.pil_image = Image.open(image_path)
            
            # Get image info
            self.width, self.height = self.pil_image.size
            self.format = self.pil_image.format
            self.total_pixels = self.width * self.height
            
            # Calculate file size
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
        """Return current image information"""
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