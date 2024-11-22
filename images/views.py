from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UploadedImage
from .serializers import UploadedImageSerializer
from .tasks import generate_tiles_task

def index(request):
    return HttpResponse("Welcome to the Image Viewer Backend!")

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            
            # Trigger asynchronous tile generation
            generate_tiles_task.delay(image.id)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageListView(APIView):
    def get(self, request, *args, **kwargs):
        images = UploadedImage.objects.all()
        serializer = UploadedImageSerializer(images, many=True)
        return Response(serializer.data)
