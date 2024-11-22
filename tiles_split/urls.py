from django.urls import path
from . import views

urlpatterns = [
    path('generate_tiles/<int:image_id>/', views.generate_tiles, name='generate_tiles'),
    path('get_tile/<int:image_id>/<int:x>/<int:y>/', views.get_tile, name='get_tile'), ###
]
