import os
from django.http import JsonResponse, FileResponse
from django.conf import settings
from .models import LargeImage
from .utils import split_image_into_tiles

def generate_tiles(request, image_id):
    """
    Генерирует тайлы для изображения.
    """
    tile_size = int(request.GET.get('tile_size', 256))
    image_obj = LargeImage.objects.get(id=image_id)
    image_path = image_obj.image.path

    output_dir = os.path.join(settings.MEDIA_ROOT, f"tiles/{image_id}")
    if not os.path.exists(output_dir):
        split_image_into_tiles(image_path, tile_size, output_dir)

    return JsonResponse({"message": "Tiles generated", "path": output_dir})

def get_tile(request, image_id, x, y):
    """
    Возвращает конкретный тайл.
    """
    tile_path = os.path.join(settings.MEDIA_ROOT, f"tiles/{image_id}/tile_{x}_{y}.png")
    if os.path.exists(tile_path):
        return FileResponse(open(tile_path, 'rb'), content_type='image/png')
    else:
        return JsonResponse({"error": "Tile not found"}, status=404)
