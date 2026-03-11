from PIL import Image

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
        
        # Get background color from edge pixels
        bg_color = self._detect_background_color(pil_image)
        
        # Create mask for background pixels
        mask = self._create_background_mask(pil_image, bg_color, tolerance)
        
        # Create new image with transparency
        result = Image.new('RGBA', (self.width, self.height))
        
        # Get pixel access objects
        source_pixels = pil_image.load()
        target_pixels = result.load()
        
        # Process each pixel using for loops
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                
                # Check if this pixel is in the background mask
                if mask[y][x]:  # Background
                    # Copy RGB but make transparent
                    if len(pixel) == 3:
                        r, g, b = pixel
                    else:  # RGBA
                        r, g, b = pixel[:3]
                    target_pixels[x, y] = (r, g, b, 0)
                else:  # Foreground
                    # Keep original with full opacity
                    if len(pixel) == 3:
                        r, g, b = pixel
                        target_pixels[x, y] = (r, g, b, 255)
                    else:  # RGBA (preserve original alpha)
                        target_pixels[x, y] = pixel
        
        # Apply edge smoothing
        result = self._smooth_edges(result, mask)
        
        self.removed_background_image = result
        return self.removed_background_image
    
    def _detect_background_color(self, pil_image):
        """Detect background color by sampling edge pixels"""
        width, height = pil_image.size
        pixels = pil_image.load()
        
        # Sample edge pixels (top, bottom, left, right)
        edge_pixels = []
        
        # Sample step - take approximately 20 samples per edge
        x_step = max(1, width // 20)
        y_step = max(1, height // 20)
        
        # Top edge
        for x in range(0, width, x_step):
            edge_pixels.append(pixels[x, 0])
        
        # Bottom edge
        for x in range(0, width, x_step):
            edge_pixels.append(pixels[x, height-1])
        
        # Left edge
        for y in range(0, height, y_step):
            edge_pixels.append(pixels[0, y])
        
        # Right edge
        for y in range(0, height, y_step):
            edge_pixels.append(pixels[width-1, y])
        
        # Group similar colors
        color_groups = []
        grouping_tolerance = 20
        
        for pixel in edge_pixels:
            # Extract RGB values (ignore alpha if present)
            if len(pixel) >= 3:
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                r = g = b = pixel[0]
            
            found_group = False
            
            for group in color_groups:
                # Get representative color of group (first pixel)
                gr, gg, gb = group[0]
                
                # Check if similar
                if (abs(r - gr) <= grouping_tolerance and
                    abs(g - gg) <= grouping_tolerance and
                    abs(b - gb) <= grouping_tolerance):
                    group.append((r, g, b))
                    found_group = True
                    break
            
            if not found_group:
                color_groups.append([(r, g, b)])
        
        # Find the largest group
        largest_group = max(color_groups, key=len)
        
        # Calculate average color of the largest group
        sum_r = sum_g = sum_b = 0
        for r, g, b in largest_group:
            sum_r += r
            sum_g += g
            sum_b += b
        
        count = len(largest_group)
        bg_color = (sum_r // count, sum_g // count, sum_b // count)
        
        return bg_color
    
    def _create_background_mask(self, pil_image, bg_color, tolerance):
        """Create mask where True indicates background pixels"""
        width, height = pil_image.size
        pixels = pil_image.load()
        
        # Create 2D mask as list of lists
        mask = [[False for _ in range(width)] for _ in range(height)]
        
        # First pass: identify pixels similar to background color
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                
                # Extract RGB
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                else:
                    r = g = b = pixel[0]
                
                # Calculate color distance (Manhattan distance)
                distance = (abs(r - bg_color[0]) + 
                           abs(g - bg_color[1]) + 
                           abs(b - bg_color[2]))
                
                # Mark as potential background if within tolerance
                if distance <= tolerance * 3:  # *3 because we summed 3 channels
                    mask[y][x] = True
        
        # Flood fill from edges to capture connected background
        visited = [[False for _ in range(width)] for _ in range(height)]
        queue = []
        
        # Add edge pixels that are potential background to queue
        # Top and bottom edges
        for y in [0, height-1]:
            for x in range(width):
                if mask[y][x] and not visited[y][x]:
                    queue.append((y, x))
                    visited[y][x] = True
        
        # Left and right edges
        for x in [0, width-1]:
            for y in range(height):
                if mask[y][x] and not visited[y][x]:
                    queue.append((y, x))
                    visited[y][x] = True
        
        # Perform flood fill (BFS)
        while queue:
            y, x = queue.pop(0)  # Pop from front (FIFO)
            
            # Check four neighbors
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                
                # Check if neighbor is within bounds
                if 0 <= ny < height and 0 <= nx < width:
                    # If neighbor is potential background and not visited
                    if mask[ny][nx] and not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((ny, nx))
        
        return visited
    
    def _smooth_edges(self, pil_image, mask):
        """Apply smoothing to edges for better transparency transitions"""
        width, height = pil_image.size
        pixels = pil_image.load()
        
        # Create result image with transparency
        result = Image.new('RGBA', (width, height))
        result_pixels = result.load()
        
        # First, copy all pixels with their original alpha
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if len(pixel) == 3:
                    r, g, b = pixel
                    result_pixels[x, y] = (r, g, b, 255)
                else:  # RGBA
                    result_pixels[x, y] = pixel
        
        # Simple edge smoothing: for edge pixels, make semi-transparent
        # based on number of background neighbors
        feather_distance = 3  # Smaller feather for performance
        
        for y in range(height):
            for x in range(width):
                # If this is a background pixel according to mask, skip
                if mask[y][x]:
                    continue
                
                # Check if this foreground pixel touches background
                bg_neighbors = 0
                total_neighbors = 0
                
                # Check 3x3 neighborhood
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            total_neighbors += 1
                            if mask[ny][nx]:
                                bg_neighbors += 1
                
                # If pixel has background neighbors, it's on the edge
                if bg_neighbors > 0:
                    # Calculate transparency based on ratio of background neighbors
                    alpha_ratio = 1.0 - (bg_neighbors / total_neighbors)
                    alpha = int(alpha_ratio * 255)
                    
                    # Get current pixel
                    r, g, b, _ = result_pixels[x, y]
                    result_pixels[x, y] = (r, g, b, alpha)
        
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
        
        pixels = self.removed_background_image.load()
        
        transparent_pixels = 0
        opaque_pixels = 0
        semi_transparent = 0
        
        for y in range(self.height):
            for x in range(self.width):
                pixel = pixels[x, y]
                if len(pixel) == 4:
                    alpha = pixel[3]
                    if alpha == 0:
                        transparent_pixels += 1
                    elif alpha == 255:
                        opaque_pixels += 1
                    else:
                        semi_transparent += 1
        
        total_pixels = self.width * self.height
        
        return {
            'transparent_pixels': transparent_pixels,
            'opaque_pixels': opaque_pixels,
            'semi_transparent_pixels': semi_transparent,
            'transparent_percentage': (transparent_pixels / total_pixels) * 100,
            'opaque_percentage': (opaque_pixels / total_pixels) * 100,
            'width': self.width,
            'height': self.height,
            'total_pixels': total_pixels
        }