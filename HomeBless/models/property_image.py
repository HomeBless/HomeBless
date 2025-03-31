from django.db import models
from .property import Property
import os


def property_image_upload_path(instance, filename):
    return os.path.join('property_images', str(instance.property.id), filename)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=property_image_upload_path)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.title}"
