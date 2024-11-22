from django.db import models
from PIL import Image
import os

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')  # Path for uploaded images
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return f"Uploaded Image {self.id}"

    def generate_tiles(self, tile_size=256):
        """
        Generate image tiles for seamless viewing.
        """
        try:
            from pathlib import Path
            import deepzoom  # Ensure this is installed: `pip install deepzoom`

            # Input image path
            input_path = self.image.path

            # Output directory for tiles
            output_dir = Path(self.image.path).parent / "tiles" / str(self.id)

            # Create the output directory if it doesn't exist
            if not output_dir.exists():
                os.makedirs(output_dir)

            # Use the deepzoom library to create tiles
            creator = deepzoom.ImageCreator(tile_size=tile_size, tile_overlap=0, tile_format="png")
            creator.create(input_path, str(output_dir))

        except Exception as e:
            raise RuntimeError(f"Error generating tiles for image {self.id}: {e}")
