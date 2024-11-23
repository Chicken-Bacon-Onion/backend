from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.conf import settings
import os
from PIL import Image
from .models import UploadedImage
from .utils import generate_tiles

class ImageUploadView(APIView):
    """
    Handles image uploads and generates Deep Zoom tiles.
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('image')
        source = request.data.get('source', 'none')

        if not file_obj:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and process the image format
        try:
            img = Image.open(file_obj)
            format = img.format
            if format not in ['TIFF', 'PNG']:
                return Response({"error": "Unsupported image format."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error processing image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded image to the database
        uploaded_image = UploadedImage.objects.create(
            image=file_obj,
            source=source,
            format=format
        )

        # Generate Deep Zoom tiles
        try:
            image_path = uploaded_image.image.path
            output_dir = os.path.join(settings.MEDIA_ROOT, 'dzi', str(uploaded_image.id))
            os.makedirs(output_dir, exist_ok=True)

            generate_tiles(image_path, output_dir)
        except Exception as e:
            return Response({"error": f"Error generating tiles: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return a simplified response with metadata
        response_data = {
            "id": uploaded_image.id,
            "image": uploaded_image.image.url,
            "upload_time": uploaded_image.upload_time,
            "source": uploaded_image.source,
            "format": uploaded_image.format,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
