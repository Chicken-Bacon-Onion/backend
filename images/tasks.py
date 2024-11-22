from celery import shared_task
from .models import UploadedImage

@shared_task
def generate_tiles_task(image_id):
    try:
        image = UploadedImage.objects.get(id=image_id)
        image.generate_tiles()
    except UploadedImage.DoesNotExist:
        pass
