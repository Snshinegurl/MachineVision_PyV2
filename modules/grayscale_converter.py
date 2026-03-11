from PIL import Image
from modules.pixel_stats import PixelStats   # new impor

class GrayscaleConverter:
    def __init__(self):
        self.grayscale_image = None
        self.width = 0
        self.height = 0
    
    def convert_to_grayscale(self, pil_image):
        """Convert PIL Image to grayscale using manual pixel processing."""
        if not pil_image:
            return None
        
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        gray_image = Image.new('RGB', (self.width, self.height))
        source_pixels = pil_image.load()
        target_pixels = gray_image.load()
        
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                elif len(pixel) == 1:
                    r = g = b = pixel[0]
                else:
                    r = g = b = 0
                
                gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
                if gray_value < 0:
                    gray_value = 0
                elif gray_value > 255:
                    gray_value = 255
                
                target_pixels[x, y] = (gray_value, gray_value, gray_value)
        
        self.grayscale_image = gray_image
        return self.grayscale_image
    
    def convert_manual_loop(self, pil_image):
        """Optimized manual pixel loop using integer arithmetic."""
        if not pil_image:
            return None
        
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        gray_image = Image.new('RGB', (self.width, self.height))
        source_pixels = pil_image.load()
        target_pixels = gray_image.load()
        
        r_factor = 299
        g_factor = 587
        b_factor = 114
        
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                elif len(pixel) == 1:
                    r = g = b = pixel[0]
                else:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                
                gray_value = (r * r_factor + g * g_factor + b * b_factor) // 1000
                if gray_value > 255:
                    gray_value = 255
                
                target_pixels[x, y] = (gray_value, gray_value, gray_value)
        
        self.grayscale_image = gray_image
        return self.grayscale_image
    
    def convert_with_compatibility(self, pil_image):
        """Handle various image modes."""
        if not pil_image:
            return None
        
        if pil_image.mode == 'L':
            self.width, self.height = pil_image.size
            self.grayscale_image = pil_image.copy()
            return self.grayscale_image
        elif pil_image.mode == 'RGB':
            return self.convert_manual_loop(pil_image)
        elif pil_image.mode == 'RGBA':
            rgb_image = Image.new('RGB', pil_image.size)
            rgb_pixels = rgb_image.load()
            source_pixels = pil_image.load()
            for y in range(pil_image.height):
                for x in range(pil_image.width):
                    r, g, b, a = source_pixels[x, y]
                    rgb_pixels[x, y] = (r, g, b)
            return self.convert_manual_loop(rgb_image)
        elif pil_image.mode == 'CMYK':
            rgb_image = Image.new('RGB', pil_image.size)
            rgb_pixels = rgb_image.load()
            source_pixels = pil_image.load()
            for y in range(pil_image.height):
                for x in range(pil_image.width):
                    c, m, y_, k = source_pixels[x, y]
                    r = 255 - (c + k)
                    g = 255 - (m + k)
                    b = 255 - (y_ + k)
                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))
                    rgb_pixels[x, y] = (r, g, b)
            return self.convert_manual_loop(rgb_image)
        else:
            rgb_image = pil_image.convert('RGB')
            return self.convert_manual_loop(rgb_image)
    
    def get_grayscale_stats(self):
        """Get statistics using PixelStats utility."""
        if not self.grayscale_image:
            return None
        
        stats = PixelStats.get_grayscale_stats(self.grayscale_image)
        if stats:
            stats['width'] = self.width
            stats['height'] = self.height
        return stats
    
    def get_histogram(self):
        """Get histogram using PixelStats."""
        if not self.grayscale_image:
            return None
        return PixelStats.get_histogram(self.grayscale_image)
    
    def get_brightness_info(self):
        """Get brightness classification based on mean value."""
        stats = self.get_grayscale_stats()
        if not stats:
            return None
        
        mean_val = stats['mean']
        if mean_val < 85:
            category = "Dark"
            description = "Image is predominantly dark"
        elif mean_val < 170:
            category = "Medium"
            description = "Image has balanced brightness"
        else:
            category = "Bright"
            description = "Image is predominantly bright"
        
        return {
            'mean_brightness': mean_val,
            'category': category,
            'description': description,
            'contrast': stats['std']
        }