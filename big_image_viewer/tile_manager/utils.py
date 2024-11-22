from PIL import Image
import os

def split_image_into_tiles(image_path, tile_size, output_dir):
    """
    Разбивает изображение на тайлы.
    :param image_path: Путь к исходному изображению.
    :param tile_size: Размер одной стороны тайла.
    :param output_dir: Каталог для сохранения тайлов.
    """
    image = Image.open(image_path)
    width, height = image.size
    os.makedirs(output_dir, exist_ok=True)

    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            box = (x, y, x + tile_size, y + tile_size)
            tile = image.crop(box)
            tile_filename = f"{output_dir}/tile_{x}_{y}.png"
            tile.save(tile_filename)
