from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UploadedImage
from .tasks import process_image

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.data.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save file metadata to database
        uploaded_image = UploadedImage.objects.create(image=file_obj)

        # Trigger background task to process the image
        process_image.delay(uploaded_image.id)

        return Response({'message': 'File uploaded successfully and processing started'}, status=status.HTTP_201_CREATED)
