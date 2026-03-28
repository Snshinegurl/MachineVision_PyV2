from PIL import Image
from modules.pixel_stats import PixelStats
from modules.pixel_processor import process_pixels

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

        # 1. Detect background color from edges (manual loop)
        bg_color = self._detect_background_color(pil_image)

        # 2. Create mask image (1‑channel) using process_pixels
        def mask_transform(x, y, pixel):
            if len(pixel) >= 3:
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                r = g = b = pixel[0]
            distance = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])
            # Return 1 if background, else 0 (we'll store as a 1‑channel image)
            return (1 if distance <= tolerance * 3 else 0,)

        # Create a 1‑channel mask image ('L' mode)
        mask_img = process_pixels(pil_image, mask_transform, output_mode='L')
        # Convert mask to a 2D list of booleans for flood fill
        mask_pixels = mask_img.load()
        mask = [[False for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                mask[y][x] = (mask_pixels[x, y] == 1)

        # 3. Flood fill from borders (manual BFS)
        visited = self._flood_fill_mask(mask)

        # 4. Create RGBA image with transparency using process_pixels
        def rgba_transform(x, y, pixel):
            if len(pixel) >= 3:
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                r = g = b = pixel[0]
            alpha = 0 if visited[y][x] else 255
            return (r, g, b, alpha)

        rgba_img = process_pixels(pil_image, rgba_transform, output_mode='RGBA')

        # 5. Smooth edges (manual loops, but we can also use process_pixels with neighbor access)
        smoothed = self._smooth_edges(rgba_img, visited)

        self.removed_background_image = smoothed
        return self.removed_background_image

    def _detect_background_color(self, pil_image):
        """Detect background color by sampling edge pixels (manual loops)."""
        width, height = pil_image.size
        pixels = pil_image.load()
        edge_pixels = []
        x_step = max(1, width // 20)
        y_step = max(1, height // 20)

        for x in range(0, width, x_step):
            edge_pixels.append(pixels[x, 0])
            edge_pixels.append(pixels[x, height-1])
        for y in range(0, height, y_step):
            edge_pixels.append(pixels[0, y])
            edge_pixels.append(pixels[width-1, y])

        # Group similar colors (simple clustering)
        color_groups = []
        grouping_tolerance = 20
        for pixel in edge_pixels:
            if len(pixel) >= 3:
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                r = g = b = pixel[0]
            found = False
            for group in color_groups:
                gr, gg, gb = group[0]
                if (abs(r - gr) <= grouping_tolerance and
                    abs(g - gg) <= grouping_tolerance and
                    abs(b - gb) <= grouping_tolerance):
                    group.append((r, g, b))
                    found = True
                    break
            if not found:
                color_groups.append([(r, g, b)])

        largest_group = max(color_groups, key=len)
        sum_r = sum_g = sum_b = 0
        for r, g, b in largest_group:
            sum_r += r
            sum_g += g
            sum_b += b
        count = len(largest_group)
        return (sum_r // count, sum_g // count, sum_b // count)

    def _flood_fill_mask(self, mask):
        """BFS flood fill from borders to keep only background connected to edges."""
        h, w = len(mask), len(mask[0])
        visited = [[False for _ in range(w)] for _ in range(h)]
        queue = []
        # Add border cells that are True in mask
        for y in range(h):
            if mask[y][0] and not visited[y][0]:
                queue.append((y, 0))
                visited[y][0] = True
            if mask[y][w-1] and not visited[y][w-1]:
                queue.append((y, w-1))
                visited[y][w-1] = True
        for x in range(w):
            if mask[0][x] and not visited[0][x]:
                queue.append((0, x))
                visited[0][x] = True
            if mask[h-1][x] and not visited[h-1][x]:
                queue.append((h-1, x))
                visited[h-1][x] = True

        # BFS
        while queue:
            y, x = queue.pop(0)
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    if mask[ny][nx] and not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((ny, nx))
        return visited

    def _smooth_edges(self, rgba_img, mask):
        """Apply edge smoothing by adjusting alpha based on neighbor mask."""
        width, height = rgba_img.size
        pixels = rgba_img.load()
        result = Image.new('RGBA', (width, height))
        result_pixels = result.load()
        # Copy original pixels first
        for y in range(height):
            for x in range(width):
                result_pixels[x, y] = pixels[x, y]

        feather_distance = 3
        for y in range(height):
            for x in range(width):
                if mask[y][x]:
                    continue
                bg_neighbors = 0
                total = 0
                for dy in range(-feather_distance, feather_distance+1):
                    for dx in range(-feather_distance, feather_distance+1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            total += 1
                            if mask[ny][nx]:
                                bg_neighbors += 1
                if bg_neighbors > 0:
                    alpha_ratio = 1.0 - (bg_neighbors / total)
                    alpha = int(alpha_ratio * 255)
                    r, g, b, _ = result_pixels[x, y]
                    result_pixels[x, y] = (r, g, b, alpha)
        return result

    # The rest of the methods (remove_background_simple, get_stats) remain unchanged
    # and are included below.

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