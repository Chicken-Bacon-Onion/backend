# tile_manager/admin.py
from django.contrib import admin
from .models import Image

@admin.register(Image)
class LargeImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at')
