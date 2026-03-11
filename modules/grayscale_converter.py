from PIL import Image

class GrayscaleConverter:
    def __init__(self):
        self.grayscale_image = None
        self.width = 0
        self.height = 0
    
    def convert_to_grayscale(self, pil_image):
        """
        Convert PIL Image to grayscale using manual pixel processing
        This method does NOT use PIL's convert('L') method
        This version uses pure Python loops (no NumPy)
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
        
        # Process each pixel using nested loops
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                
                # Extract RGB values (handle different formats)
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                elif len(pixel) == 1:
                    r = g = b = pixel[0]
                else:  # Should not happen after conversion, but just in case
                    r = g = b = 0
                
                # Apply luminosity method: 0.299R + 0.587G + 0.114B
                # Using floating point arithmetic
                gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # Ensure value is in 0-255 range
                if gray_value < 0:
                    gray_value = 0
                elif gray_value > 255:
                    gray_value = 255
                
                # Set pixel (all three channels same for grayscale)
                target_pixels[x, y] = (gray_value, gray_value, gray_value)
        
        self.grayscale_image = gray_image
        return self.grayscale_image
    
    def convert_manual_loop(self, pil_image):
        """
        Optimized manual pixel loop using integer arithmetic and direct pixel access
        Fastest possible without NumPy (already no NumPy in this method)
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
    
    def convert_with_compatibility(self, pil_image):
        """
        Additional method that handles all image modes and provides
        maximum compatibility with different input formats
        """
        if not pil_image:
            return None
        
        # Handle different modes explicitly
        if pil_image.mode == 'L':
            # Already grayscale - just copy
            self.width, self.height = pil_image.size
            self.grayscale_image = pil_image.copy()
            return self.grayscale_image
        
        elif pil_image.mode == 'RGB':
            # Standard RGB - use manual loop
            return self.convert_manual_loop(pil_image)
        
        elif pil_image.mode == 'RGBA':
            # RGB with alpha - convert to RGB first (drop alpha)
            rgb_image = Image.new('RGB', pil_image.size)
            rgb_pixels = rgb_image.load()
            source_pixels = pil_image.load()
            
            for y in range(pil_image.height):
                for x in range(pil_image.width):
                    r, g, b, a = source_pixels[x, y]
                    rgb_pixels[x, y] = (r, g, b)
            
            return self.convert_manual_loop(rgb_image)
        
        elif pil_image.mode == 'CMYK':
            # CMYK to RGB conversion (simplified)
            rgb_image = Image.new('RGB', pil_image.size)
            rgb_pixels = rgb_image.load()
            source_pixels = pil_image.load()
            
            for y in range(pil_image.height):
                for x in range(pil_image.width):
                    c, m, y_, k = source_pixels[x, y]
                    # Simplified CMYK to RGB
                    r = 255 - (c + k)
                    g = 255 - (m + k)
                    b = 255 - (y_ + k)
                    # Clamp values
                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))
                    rgb_pixels[x, y] = (r, g, b)
            
            return self.convert_manual_loop(rgb_image)
        
        else:
            # For other modes, let PIL handle conversion to RGB
            rgb_image = pil_image.convert('RGB')
            return self.convert_manual_loop(rgb_image)
    
    def get_grayscale_stats(self):
        """Get statistics about the grayscale conversion without NumPy"""
        if not self.grayscale_image:
            return None
        
        # Convert to single channel 'L' mode for easier processing
        gray_img = self.grayscale_image.convert('L')
        pixels = gray_img.load()
        
        # Initialize variables for statistics
        min_val = 255
        max_val = 0
        sum_val = 0
        sum_squared = 0
        total_pixels = self.width * self.height
        
        # Calculate min, max, sum in one pass
        for y in range(self.height):
            for x in range(self.width):
                val = pixels[x, y]
                
                # Update min and max
                if val < min_val:
                    min_val = val
                if val > max_val:
                    max_val = val
                
                # Add to sum for mean calculation
                sum_val += val
                
                # Add square for standard deviation
                sum_squared += val * val
        
        # Calculate mean
        mean_val = sum_val / total_pixels if total_pixels > 0 else 0
        
        # Calculate standard deviation
        # Formula: sqrt( (sum(x^2)/n) - (mean)^2 )
        if total_pixels > 0:
            variance = (sum_squared / total_pixels) - (mean_val * mean_val)
            std_val = variance ** 0.5  # Square root
        else:
            std_val = 0
        
        return {
            'min': min_val,
            'max': max_val,
            'mean': mean_val,
            'std': std_val,
            'width': self.width,
            'height': self.height,
            'total_pixels': total_pixels
        }
    
    def get_histogram(self):
        """
        Get histogram of grayscale values (0-255)
        Returns a list of 256 integers
        """
        if not self.grayscale_image:
            return None
        
        # Convert to single channel 'L' mode
        gray_img = self.grayscale_image.convert('L')
        pixels = gray_img.load()
        
        # Initialize histogram with 256 bins
        histogram = [0] * 256
        
        # Count pixels in each bin
        for y in range(self.height):
            for x in range(self.width):
                val = pixels[x, y]
                histogram[val] += 1
        
        return histogram
    
    def get_brightness_info(self):
        """
        Get brightness classification based on mean value
        """
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