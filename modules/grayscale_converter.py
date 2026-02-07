from PIL import Image
import numpy as np

class GrayscaleConverter:
    def __init__(self):
        self.grayscale_image = None
        self.width = 0
        self.height = 0
    
    def convert_to_grayscale(self, pil_image):
        """
        Convert PIL Image to grayscale using manual pixel processing
        This method does NOT use PIL's convert('L') method
        """
        if not pil_image:
            return None
        
        # Convert to RGB if necessary
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        
        # Convert to numpy array for faster processing
        img_array = np.array(pil_image)
        
        # Extract RGB channels
        if len(img_array.shape) == 3:
            r = img_array[:, :, 0]
            g = img_array[:, :, 1]
            b = img_array[:, :, 2]
            
            # Apply luminosity method (standard grayscale conversion)
            # Using integer arithmetic for precision
            gray_values = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
            
            # Create 3-channel grayscale image
            gray_array = np.stack([gray_values, gray_values, gray_values], axis=2)
        else:
            # Already single channel
            gray_array = img_array
        
        # Convert back to PIL Image
        self.grayscale_image = Image.fromarray(gray_array)
        return self.grayscale_image
    
    def convert_manual_loop(self, pil_image):
        """
        Optimized manual pixel loop using integer arithmetic and direct pixel access
        Fastest possible without NumPy
        """
        if not pil_image:
            return None
        
        # Convert to RGB if necessary
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        
        # Create new image for grayscale
        gray_image = Image.new('RGB', (self.width, self.height))
        
        # Get pixel access objects
        source_pixels = pil_image.load()
        target_pixels = gray_image.load()
        
        # Use integer arithmetic for faster calculations
        # Convert floats to integers: 0.299 * 1000 = 299, etc.
        r_factor = 299   # 0.299 * 1000
        g_factor = 587   # 0.587 * 1000
        b_factor = 114   # 0.114 * 1000
        
        # Process each pixel using direct pixel access
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                
                # Handle different pixel formats
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                elif len(pixel) == 1:
                    r = g = b = pixel[0]
                else:  # RGBA
                    r, g, b = pixel[0], pixel[1], pixel[2]
                
                # Luminosity method using integer arithmetic
                # (r * 299 + g * 587 + b * 114) // 1000
                gray_value = (r * r_factor + g * g_factor + b * b_factor) // 1000
                
                # Ensure value is in 0-255 range
                if gray_value > 255:
                    gray_value = 255
                
                # Set pixel directly
                target_pixels[x, y] = (gray_value, gray_value, gray_value)
        
        self.grayscale_image = gray_image
        return self.grayscale_image
    
    def get_grayscale_stats(self):
        """Get statistics about the grayscale conversion"""
        if not self.grayscale_image:
            return None
        
        gray_array = np.array(self.grayscale_image.convert('L'))
        
        return {
            'min': int(gray_array.min()),
            'max': int(gray_array.max()),
            'mean': float(gray_array.mean()),
            'std': float(gray_array.std()),
            'width': self.width,
            'height': self.height,
            'total_pixels': self.width * self.height
        }