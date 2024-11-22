from django.contrib import admin
from .models import UploadedImage

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at')  # Include the uploaded_at field
