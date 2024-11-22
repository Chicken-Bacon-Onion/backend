from django.db import models

class LargeImage(models.Model):
    image = models.ImageField(upload_to='large_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)