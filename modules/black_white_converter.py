from PIL import Image
from modules.grayscale_converter import GrayscaleConverter

class BlackWhiteConverter:
    def __init__(self):
        self.black_white_image = None
        self.width = 0
        self.height = 0
        self.grayscale_converter = GrayscaleConverter()
        self.threshold = 128  # Default threshold
    
    def convert_to_black_white(self, pil_image, threshold=None, method='manual'):
        """
        Convert PIL Image to black and white using thresholding
        Reuses the grayscale conversion from GrayscaleConverter
        
        Parameters:
        - pil_image: Input PIL Image
        - threshold: Threshold value (0-255). If None, will be calculated based on method
        - method: 'manual' (fixed threshold), 'otsu' (automatic Otsu's method)
        """
        if not pil_image:
            return None
        
        # First, convert to grayscale using the GrayscaleConverter's manual loop
        grayscale_image = self.grayscale_converter.convert_manual_loop(pil_image)
        
        if not grayscale_image:
            return None
        
        self.width, self.height = grayscale_image.size
        
        # Determine threshold based on method
        if threshold is not None:
            self.threshold = threshold
        elif method == 'otsu':
            self.threshold = self._calculate_otsu_threshold(grayscale_image)
        else:
            self.threshold = 128  # Default fixed threshold
        
        # Create new image for black and white
        bw_image = Image.new('RGB', (self.width, self.height))
        
        # Get pixel access objects
        source_pixels = grayscale_image.load()
        target_pixels = bw_image.load()
        
        # Process each pixel to convert to black/white based on threshold
        for y in range(self.height):
            for x in range(self.width):
                # Get the gray value from grayscale image
                gray_value = source_pixels[x, y][0]  # All channels are same in grayscale
                
                # **Thresholding Logic:**
                # - If Pixel Value < Threshold: Change to Black (0)
                # - If Pixel Value ≥ Threshold: Change to White (255)
                if gray_value < self.threshold:
                    bw_value = 0    # Black
                else:
                    bw_value = 255  # White
                
                # Set pixel as black or white (all RGB channels same)
                target_pixels[x, y] = (bw_value, bw_value, bw_value)
        
        self.black_white_image = bw_image
        return self.black_white_image
    
    def _calculate_otsu_threshold(self, grayscale_image):
        """
        Calculate optimal threshold using Otsu's method
        Otsu's Method (Automated): Analyzes the image histogram to find the best 
        threshold to distinguish foreground from background
        
        Parameters:
        - grayscale_image: Grayscale PIL Image
        
        Returns:
        - Optimal threshold value (0-255)
        """
        # Get histogram of grayscale values (0-255)
        histogram = grayscale_image.histogram()
        total_pixels = sum(histogram)
        
        if total_pixels == 0:
            return 128  # Default if no pixels
        
        # Calculate total sum for mean calculation
        sum_total = 0
        for i in range(256):
            sum_total += i * histogram[i]
        
        # Variables for Otsu's calculation
        sum_back = 0        # Sum of background pixels
        weight_back = 0     # Weight of background
        weight_fore = 0     # Weight of foreground
        
        variance_max = 0    # Maximum between-class variance
        optimal_threshold = 128  # Default optimal threshold
        
        # Iterate through all possible threshold values
        for threshold in range(256):
            # Add current threshold's pixels to background
            weight_back += histogram[threshold]
            
            if weight_back == 0:
                continue  # Skip if no background pixels yet
            
            # Calculate foreground weight
            weight_fore = total_pixels - weight_back
            
            if weight_fore == 0:
                break  # All pixels are in background
            
            # Add to sum of background
            sum_back += threshold * histogram[threshold]
            
            # Calculate means
            mean_back = sum_back / weight_back
            mean_fore = (sum_total - sum_back) / weight_fore
            
            # Calculate between-class variance
            variance_between = weight_back * weight_fore * (mean_back - mean_fore) ** 2
            
            # Update optimal threshold if variance is higher
            if variance_between > variance_max:
                variance_max = variance_between
                optimal_threshold = threshold
        
        return optimal_threshold
    
    def convert_with_multiple_thresholds(self, pil_image, low_threshold=85, high_threshold=170):
        """
        Convert to black and white with three levels: Black, Gray, White
        Uses two threshold values
        
        Parameters:
        - pil_image: Input PIL Image
        - low_threshold: Threshold between black and gray
        - high_threshold: Threshold between gray and white
        
        Returns:
        - PIL Image with three levels (0, 128, 255)
        """
        if not pil_image:
            return None
        
        # First, convert to grayscale
        grayscale_image = self.grayscale_converter.convert_manual_loop(pil_image)
        
        if not grayscale_image:
            return None
        
        self.width, self.height = grayscale_image.size
        
        # Create new image
        three_level_image = Image.new('RGB', (self.width, self.height))
        
        # Get pixel access objects
        source_pixels = grayscale_image.load()
        target_pixels = three_level_image.load()
        
        # Process each pixel with two thresholds
        for y in range(self.height):
            for x in range(self.width):
                gray_value = source_pixels[x, y][0]
                
                # Apply dual threshold logic
                if gray_value < low_threshold:
                    level_value = 0      # Black
                elif gray_value < high_threshold:
                    level_value = 128    # Gray
                else:
                    level_value = 255    # White
                
                target_pixels[x, y] = (level_value, level_value, level_value)
        
        self.black_white_image = three_level_image
        return self.black_white_image
    
    def get_threshold_info(self):
        """Get information about the threshold used"""
        return {
            'threshold': self.threshold,
            'threshold_description': self._get_threshold_description()
        }
    
    def _get_threshold_description(self):
        """Get a description of the threshold value"""
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
        """
        Get statistics about the black and white conversion
        
        Returns:
        - Dictionary with black/white pixel counts and percentages
        """
        if not self.black_white_image:
            return None
        
        # Initialize counters
        black_count = 0
        white_count = 0
        
        # Get pixel data
        pixels = self.black_white_image.load()
        
        # Count black and white pixels
        for y in range(self.height):
            for x in range(self.width):
                pixel_value = pixels[x, y][0]
                if pixel_value < 128:  # Consider values < 128 as black
                    black_count += 1
                else:  # Values >= 128 as white
                    white_count += 1
        
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
        """
        Create a visualization showing the threshold on the histogram
        
        Returns:
        - PIL Image showing histogram with threshold line
        """
        if not pil_image:
            return None
        
        # Convert to grayscale first
        grayscale_image = self.grayscale_converter.convert_manual_loop(pil_image)
        
        if not grayscale_image:
            return None
        
        # Get histogram
        histogram = grayscale_image.histogram()
        
        # Create visualization image
        viz_width = 512
        viz_height = 256
        viz_image = Image.new('RGB', (viz_width, viz_height), color='white')
        draw = Image.Draw.Draw(viz_image)
        
        # Find max histogram value for scaling
        max_hist = max(histogram) if histogram else 1
        
        # Draw histogram bars
        bar_width = viz_width // 256
        for i in range(256):
            bar_height = (histogram[i] / max_hist) * (viz_height - 20)
            x1 = i * bar_width
            x2 = (i + 1) * bar_width
            y1 = viz_height - bar_height
            y2 = viz_height
            
            # Draw bar
            draw.rectangle([x1, y1, x2, y2], fill='blue')
        
        # Draw threshold line
        threshold_x = self.threshold * bar_width
        draw.line([threshold_x, 0, threshold_x, viz_height], fill='red', width=2)
        
        # Add text
        draw.text((10, 10), f"Threshold: {self.threshold}", fill='black')
        draw.text((10, 30), f"Method: {'Otsu' if self.threshold != 128 else 'Fixed'}", fill='black')
        
        return viz_image