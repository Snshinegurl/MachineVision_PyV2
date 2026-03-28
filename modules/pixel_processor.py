from PIL import Image

def get_image_info(pil_image):
    """
    Return (width, height, channels, total_pixels, mode)
    using PIL attributes (no numpy).
    """
    width, height = pil_image.size
    mode = pil_image.mode
    # Map mode to number of channels (common modes)
    channel_map = {
        '1': 1, 'L': 1, 'P': 1,
        'RGB': 3, 'RGBA': 4,
        'CMYK': 4, 'YCbCr': 3, 'LAB': 3
    }
    channels = channel_map.get(mode, 1)
    total_pixels = width * height
    return width, height, channels, total_pixels, mode

def process_pixels(pil_image, pixel_transform, output_mode='RGB'):
    """
    Iterate over each pixel of the input PIL image, apply pixel_transform,
    and return a new PIL image of the specified output_mode.

    Args:
        pil_image (PIL.Image): Input image (will be converted to RGB if needed).
        pixel_transform (callable): Function that takes (x, y, pixel) and returns
                                    a tuple of values for the output pixel.
        output_mode (str): Mode of the output image (e.g., 'RGB', 'RGBA', 'L').

    Returns:
        PIL.Image: New image with transformed pixels.
    """
    # Ensure we have RGB or RGBA for consistent pixel access
    if pil_image.mode not in ('RGB', 'RGBA'):
        pil_image = pil_image.convert('RGB')

    width, height = pil_image.size
    src = pil_image.load()

    # Create output image
    result = Image.new(output_mode, (width, height))
    dst = result.load()

    # Manual double loop – every pixel is processed individually
    for y in range(height):
        for x in range(width):
            pixel = src[x, y]
            new_pixel = pixel_transform(x, y, pixel)
            dst[x, y] = new_pixel

    return result