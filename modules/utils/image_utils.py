import os
from PIL import Image

class ImageUtils:
    @staticmethod
    def get_image_info(image_path):
        """Get basic image information"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                format = img.format
                return width, height, format
        except Exception as e:
            raise Exception(f"Failed to get image info: {str(e)}")
    
    @staticmethod
    def is_supported_format(image_path):
        """Check if image format is supported"""
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
        return image_path.lower().endswith(supported_formats)
    
    @staticmethod
    def calculate_file_size(image_path):
        """Calculate file size in bytes"""
        return os.path.getsize(image_path)
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 Bytes"
        size_names = ("Bytes", "KB", "MB", "GB")
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.2f} {size_names[i]}"