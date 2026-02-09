from PIL import Image
import numpy as np

class BackgroundRemover:
    def __init__(self):
        self.removed_background_image = None
        self.width = 0
        self.height = 0
        
    def remove_background(self, pil_image, tolerance=30):
        """
        Remove background using color similarity algorithm
        Identifies background as the most common color around the edges
        
        Parameters:
        - pil_image: Input PIL Image
        - tolerance: Color tolerance for background detection (0-255)
        """
        if not pil_image:
            return None
            
        # Convert to RGB if necessary
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        
        # Convert to numpy array for faster processing
        img_array = np.array(pil_image)
        
        # Get background color from edge pixels
        bg_color = self._detect_background_color(img_array)
        
        # Create mask for background pixels
        mask = self._create_background_mask(img_array, bg_color, tolerance)
        
        # Create transparent background (RGBA)
        result_array = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        
        # Copy RGB values from original image
        result_array[:, :, :3] = img_array
        
        # Set alpha channel: 0 for background, 255 for foreground
        result_array[:, :, 3] = np.where(mask, 0, 255)
        
        # For pixels near edges, use gradual transparency for smoother edges
        result_array = self._smooth_edges(result_array, mask)
        
        # Convert back to PIL Image
        self.removed_background_image = Image.fromarray(result_array, 'RGBA')
        return self.removed_background_image
    
    def _detect_background_color(self, img_array):
        """Detect background color by sampling edge pixels"""
        height, width = img_array.shape[:2]
        
        # Sample edge pixels (top, bottom, left, right)
        edge_pixels = []
        
        # Top edge
        for x in range(0, width, max(1, width // 20)):
            edge_pixels.append(img_array[0, x])
        
        # Bottom edge
        for x in range(0, width, max(1, width // 20)):
            edge_pixels.append(img_array[height-1, x])
        
        # Left edge
        for y in range(0, height, max(1, height // 20)):
            edge_pixels.append(img_array[y, 0])
        
        # Right edge
        for y in range(0, height, max(1, height // 20)):
            edge_pixels.append(img_array[y, width-1])
        
        # Convert to numpy array for processing
        edge_pixels = np.array(edge_pixels)
        
        # Find the most common color (simple mode by averaging similar colors)
        # Group similar colors
        color_groups = []
        tolerance = 20
        
        for pixel in edge_pixels:
            found_group = False
            for group in color_groups:
                if len(group) > 0 and np.all(np.abs(group[0] - pixel) <= tolerance):
                    group.append(pixel)
                    found_group = True
                    break
            
            if not found_group:
                color_groups.append([pixel])
        
        # Find the largest group
        largest_group = max(color_groups, key=len)
        
        # Return average color of the largest group
        return np.mean(largest_group, axis=0).astype(int)
    
    def _create_background_mask(self, img_array, bg_color, tolerance):
        """Create mask where True indicates background pixels"""
        height, width = img_array.shape[:2]
        
        # Calculate color distance for each pixel
        color_diff = np.abs(img_array - bg_color)
        color_distance = np.sum(color_diff, axis=2)
        
        # Create initial mask
        mask = color_distance <= (tolerance * 3)  # 3 channels
        
        # Apply flood fill from edges to capture all background
        visited = np.zeros((height, width), dtype=bool)
        
        # Start flood fill from edge pixels that match background
        queue = []
        for y in [0, height-1]:
            for x in range(width):
                if mask[y, x] and not visited[y, x]:
                    queue.append((y, x))
        
        for x in [0, width-1]:
            for y in range(height):
                if mask[y, x] and not visited[y, x]:
                    queue.append((y, x))
        
        # Perform flood fill
        while queue:
            y, x = queue.pop(0)
            if not visited[y, x]:
                visited[y, x] = True
                
                # Check neighbors
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < height and 0 <= nx < width:
                        if mask[ny, nx] and not visited[ny, nx]:
                            queue.append((ny, nx))
        
        return visited
    
    def _smooth_edges(self, img_array, mask):
        """Apply smoothing to edges for better transparency transitions"""
        height, width = img_array.shape[:2]
        result = img_array.copy()
        
        # Create gradient alpha for edge pixels
        from scipy import ndimage
        
        # Distance transform: distance from background
        distance = ndimage.distance_transform_edt(~mask)
        
        # Create smooth alpha transition (5 pixel feather)
        feather_distance = 5
        alpha = np.zeros((height, width), dtype=np.uint8)
        
        for y in range(height):
            for x in range(width):
                d = distance[y, x]
                if d == 0:  # Background
                    alpha[y, x] = 0
                elif d >= feather_distance:  # Definitely foreground
                    alpha[y, x] = 255
                else:  # Edge transition
                    alpha[y, x] = int((d / feather_distance) * 255)
        
        result[:, :, 3] = alpha
        return result
    
    def remove_background_simple(self, pil_image, bg_color=None, tolerance=30):
        """
        Simpler background removal for performance
        Good for images with solid color backgrounds
        """
        if not pil_image:
            return None
            
        # Convert to RGB if necessary
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        
        # Use provided background color or detect it
        if bg_color is None:
            # Simple detection: use top-left corner color
            temp_img = pil_image.copy()
            bg_color = temp_img.getpixel((0, 0))
        
        # Create new image with transparency
        result = Image.new('RGBA', (self.width, self.height))
        source_pixels = pil_image.load()
        target_pixels = result.load()
        
        # Process each pixel
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                
                # Calculate color distance
                if len(pixel) == 3:
                    r, g, b = pixel
                else:  # RGBA
                    r, g, b = pixel[:3]
                
                distance = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])
                
                if distance <= tolerance:
                    # Background - fully transparent
                    target_pixels[x, y] = (r, g, b, 0)
                else:
                    # Foreground - fully opaque
                    if len(pixel) == 3:
                        target_pixels[x, y] = (r, g, b, 255)
                    else:
                        target_pixels[x, y] = pixel
        
        self.removed_background_image = result
        return self.removed_background_image
    
    def get_stats(self):
        """Get statistics about the background removal"""
        if not self.removed_background_image:
            return None
            
        # Count transparent vs opaque pixels
        img_array = np.array(self.removed_background_image)
        alpha_channel = img_array[:, :, 3]
        
        transparent_pixels = np.sum(alpha_channel == 0)
        opaque_pixels = np.sum(alpha_channel == 255)
        semi_transparent = np.sum((alpha_channel > 0) & (alpha_channel < 255))
        
        total_pixels = self.width * self.height
        
        return {
            'transparent_pixels': int(transparent_pixels),
            'opaque_pixels': int(opaque_pixels),
            'semi_transparent_pixels': int(semi_transparent),
            'transparent_percentage': (transparent_pixels / total_pixels) * 100,
            'opaque_percentage': (opaque_pixels / total_pixels) * 100,
            'width': self.width,
            'height': self.height,
            'total_pixels': total_pixels
        }