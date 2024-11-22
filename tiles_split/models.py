from django.db import models

class UploadedImage(models.Model):
    image = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='processing')

class ImageTile(models.Model):
    uploaded_image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='tiles')
    tile = models.ImageField(upload_to='tiles/')
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()
