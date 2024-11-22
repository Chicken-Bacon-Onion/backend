# from PIL import Image
# import os
#
# def split_image_into_tiles(image_path, tile_size, output_dir):
#     """
#     Разбивает изображение на тайлы.
#     :param image_path: Путь к исходному изображению.
#     :param tile_size: Размер одной стороны тайла.
#     :param output_dir: Каталог для сохранения тайлов.
#     """
#
#     image = Image.open(image_path)
#     width, height = image.size
#     os.makedirs(output_dir, exist_ok=True)
#
#     for x in range(0, width, tile_size):
#         for y in range(0, height, tile_size):
#             box = (x, y, x + tile_size, y + tile_size)
#             tile = image.crop(box)
#             tile_filename = f"{output_dir}/tile_{x}_{y}.png"
#             tile.save(tile_filename)

# tile_manager/utils.py
from PIL import Image
import os
from multiprocessing import Pool, cpu_count

def process_tile(args):
    """
    Обрабатывает один тайл.
    :param args: Tuple (image_path, tile_size, x, y, output_dir)
    """
    image_path, tile_size, x, y, output_dir = args
    image = Image.open(image_path)
    box = (x, y, x + tile_size, y + tile_size)
    tile = image.crop(box)

    tile_filename = os.path.join(output_dir, f"tile_{x}_{y}.png")
    tile.save(tile_filename)


def split_image_into_tiles(image_path, tile_size, output_dir):
    """
    Разбивает изображение на тайлы с использованием мультипроцессинга.
    :param image_path: Путь к исходному изображению.
    :param tile_size: Размер одной стороны тайла.
    :param output_dir: Каталог для сохранения тайлов.
    """
    # Открываем изображение и определяем размеры
    image = Image.open(image_path)
    width, height = image.size

    # Убедимся, что каталог существует
    os.makedirs(output_dir, exist_ok=True)

    # Формируем задания для каждого тайла
    tasks = []
    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            tasks.append((image_path, tile_size, x, y, output_dir))

    # Используем пул процессов для обработки тайлов
    with Pool(cpu_count()) as pool:
        pool.map(process_tile, tasks)
