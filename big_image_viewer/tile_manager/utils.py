import os
from PIL import Image
import math
import multiprocessing

Image.MAX_IMAGE_PIXELS = None


def generate_tile(image, output_dir, x, y, tile_size=256):
    """
    Generate a single tile from the image.

    Args:
        image (PIL.Image): The input image object.
        output_dir (str): Directory to save the tile.
        x (int): The x index of the tile.
        y (int): The y index of the tile.
        tile_size (int): Size of each tile (default: 256).
    """
    width, height = image.size
    left = x * tile_size
    upper = y * tile_size
    right = min((x + 1) * tile_size, width)
    lower = min((y + 1) * tile_size, height)

    tile = image.crop((left, upper, right, lower))
    tile_path = os.path.join(output_dir, f"{y}_{x}.png")
    tile.convert("P", palette=Image.ADAPTIVE, colors=256)
    tile.save(tile_path, "PNG", optimize=True)


def generate_tiles(image_path, output_dir, tile_size=256):
    """
    Generate Deep Zoom tiles for the given image with multiprocessing.

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

    num_tiles_x = math.ceil(width / tile_size)
    num_tiles_y = math.ceil(height / tile_size)

    # Prepare arguments for each tile to be processed
    tasks = []
    for x in range(num_tiles_x):
        for y in range(num_tiles_y):
            tasks.append((image, output_dir, x, y, tile_size))

    # Use multiprocessing to process the tiles in parallel
    with multiprocessing.Pool() as pool:
        pool.starmap(generate_tile, tasks)

    print(f"Tiles generated in {output_dir}")
