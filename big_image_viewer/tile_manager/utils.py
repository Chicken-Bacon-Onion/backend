import os
from PIL import Image
import math


Image.MAX_IMAGE_PIXELS = None


def generate_tiles(image_path, output_dir, tile_size=256):
    """
    Generate Deep Zoom tiles for the given image.

    Args:
        image_path (str): Path to the input image.
        output_dir (str): Directory to save the tiles.
        tile_size (int): Size of each tile (default: 256).
    """
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)

    # Determine the number of zoom levels
    max_dimension = max(width, height)
    num_levels = math.ceil(math.log2(max_dimension / tile_size))

    # Generate tiles for each zoom level
    for level in range(num_levels + 1):
        scale = 2 ** level
        resized_width = math.ceil(width / scale)
        resized_height = math.ceil(height / scale)

        # Resize the image for the current zoom level
        resized_image = image.resize(
            (resized_width, resized_height),
            resample=Image.Resampling.LANCZOS  # Use LANCZOS for high-quality downsampling
        )

        # Create tiles for the current zoom level
        level_dir = os.path.join(output_dir, f"level_{level}")
        os.makedirs(level_dir, exist_ok=True)

        num_tiles_x = math.ceil(resized_width / tile_size)
        num_tiles_y = math.ceil(resized_height / tile_size)

        for x in range(num_tiles_x):
            for y in range(num_tiles_y):
                left = x * tile_size
                upper = y * tile_size
                right = min((x + 1) * tile_size, resized_width)
                lower = min((y + 1) * tile_size, resized_height)

                tile = resized_image.crop((left, upper, right, lower))
                tile_path = os.path.join(level_dir, f"{x}_{y}.jpg")
                tile.save(tile_path, "PNG", quality=80)

    print(f"Tiles generated in {output_dir}")
