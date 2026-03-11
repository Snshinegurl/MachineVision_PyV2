from PIL import Image
from modules.pixel_stats import PixelStats   # new impor

class BackgroundRemover:
    def __init__(self):
        self.removed_background_image = None
        self.width = 0
        self.height = 0
        
    def remove_background(self, pil_image, tolerance=30):
        if not pil_image:
            return None
            
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        bg_color = self._detect_background_color(pil_image)
        mask = self._create_background_mask(pil_image, bg_color, tolerance)
        result = Image.new('RGBA', (self.width, self.height))
        source_pixels = pil_image.load()
        target_pixels = result.load()
        
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                if mask[y][x]:
                    if len(pixel) == 3:
                        r, g, b = pixel
                    else:
                        r, g, b = pixel[:3]
                    target_pixels[x, y] = (r, g, b, 0)
                else:
                    if len(pixel) == 3:
                        r, g, b = pixel
                        target_pixels[x, y] = (r, g, b, 255)
                    else:
                        target_pixels[x, y] = pixel
        
        result = self._smooth_edges(result, mask)
        self.removed_background_image = result
        return self.removed_background_image
    
    def _detect_background_color(self, pil_image):
        width, height = pil_image.size
        pixels = pil_image.load()
        edge_pixels = []
        x_step = max(1, width // 20)
        y_step = max(1, height // 20)
        
        for x in range(0, width, x_step):
            edge_pixels.append(pixels[x, 0])
        for x in range(0, width, x_step):
            edge_pixels.append(pixels[x, height-1])
        for y in range(0, height, y_step):
            edge_pixels.append(pixels[0, y])
        for y in range(0, height, y_step):
            edge_pixels.append(pixels[width-1, y])
        
        color_groups = []
        grouping_tolerance = 20
        for pixel in edge_pixels:
            if len(pixel) >= 3:
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                r = g = b = pixel[0]
            found_group = False
            for group in color_groups:
                gr, gg, gb = group[0]
                if (abs(r - gr) <= grouping_tolerance and
                    abs(g - gg) <= grouping_tolerance and
                    abs(b - gb) <= grouping_tolerance):
                    group.append((r, g, b))
                    found_group = True
                    break
            if not found_group:
                color_groups.append([(r, g, b)])
        
        largest_group = max(color_groups, key=len)
        sum_r = sum_g = sum_b = 0
        for r, g, b in largest_group:
            sum_r += r
            sum_g += g
            sum_b += b
        count = len(largest_group)
        bg_color = (sum_r // count, sum_g // count, sum_b // count)
        return bg_color
    
    def _create_background_mask(self, pil_image, bg_color, tolerance):
        width, height = pil_image.size
        pixels = pil_image.load()
        mask = [[False for _ in range(width)] for _ in range(height)]
        
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                else:
                    r = g = b = pixel[0]
                distance = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])
                if distance <= tolerance * 3:
                    mask[y][x] = True
        
        visited = [[False for _ in range(width)] for _ in range(height)]
        queue = []
        for y in [0, height-1]:
            for x in range(width):
                if mask[y][x] and not visited[y][x]:
                    queue.append((y, x))
                    visited[y][x] = True
        for x in [0, width-1]:
            for y in range(height):
                if mask[y][x] and not visited[y][x]:
                    queue.append((y, x))
                    visited[y][x] = True
        
        while queue:
            y, x = queue.pop(0)
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    if mask[ny][nx] and not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((ny, nx))
        return visited
    
    def _smooth_edges(self, pil_image, mask):
        width, height = pil_image.size
        pixels = pil_image.load()
        result = Image.new('RGBA', (width, height))
        result_pixels = result.load()
        
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if len(pixel) == 3:
                    r, g, b = pixel
                    result_pixels[x, y] = (r, g, b, 255)
                else:
                    result_pixels[x, y] = pixel
        
        feather_distance = 3
        for y in range(height):
            for x in range(width):
                if mask[y][x]:
                    continue
                bg_neighbors = 0
                total_neighbors = 0
                for dy in [-1,0,1]:
                    for dx in [-1,0,1]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            total_neighbors += 1
                            if mask[ny][nx]:
                                bg_neighbors += 1
                if bg_neighbors > 0:
                    alpha_ratio = 1.0 - (bg_neighbors / total_neighbors)
                    alpha = int(alpha_ratio * 255)
                    r, g, b, _ = result_pixels[x, y]
                    result_pixels[x, y] = (r, g, b, alpha)
        return result
    
    def remove_background_simple(self, pil_image, bg_color=None, tolerance=30):
        if not pil_image:
            return None
            
        if pil_image.mode not in ('RGB', 'RGBA'):
            pil_image = pil_image.convert('RGB')
        
        self.width, self.height = pil_image.size
        if bg_color is None:
            temp_img = pil_image.copy()
            bg_color = temp_img.getpixel((0, 0))
        
        result = Image.new('RGBA', (self.width, self.height))
        source_pixels = pil_image.load()
        target_pixels = result.load()
        
        for y in range(self.height):
            for x in range(self.width):
                pixel = source_pixels[x, y]
                if len(pixel) == 3:
                    r, g, b = pixel
                else:
                    r, g, b = pixel[:3]
                distance = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])
                if distance <= tolerance:
                    target_pixels[x, y] = (r, g, b, 0)
                else:
                    if len(pixel) == 3:
                        target_pixels[x, y] = (r, g, b, 255)
                    else:
                        target_pixels[x, y] = pixel
        
        self.removed_background_image = result
        return self.removed_background_image
    
    def get_stats(self):
        if not self.removed_background_image:
            return None
        
        # Use PixelStats to count based on alpha channel
        transparent_pixels = PixelStats.count_pixels_by_condition(
            self.removed_background_image,
            lambda p: len(p) == 4 and p[3] == 0
        )
        opaque_pixels = PixelStats.count_pixels_by_condition(
            self.removed_background_image,
            lambda p: len(p) == 4 and p[3] == 255
        )
        semi_transparent = PixelStats.count_pixels_by_condition(
            self.removed_background_image,
            lambda p: len(p) == 4 and 0 < p[3] < 255
        )
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