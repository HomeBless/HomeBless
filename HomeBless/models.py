from django.db import models
from django.contrib.auth.models import User
import os


def seller_profile_picture_upload_path(instance, filename):
    """Upload profile pictures to seller_profiles/{seller_id}/{filename}"""
    return f"seller_profiles/{instance.id}/{filename}"


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)    
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    line_id = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=seller_profile_picture_upload_path, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('condominium', 'Condominium'),
        ('dorm', 'Dorm'),
        ('land', 'Land')
    ]

    SELLING_TYPE_CHOICES = [
        ('buy', 'For Sale'),
        ('rent', 'For Rent')
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    transaction_type = models.CharField(max_length=10, choices=SELLING_TYPE_CHOICES, default='buy')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    floors = models.IntegerField(null=True, blank=True)
    garages = models.IntegerField(null=True, blank=True)
    area = models.FloatField(help_text="Area in square wa")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def property_image_upload_path(instance, filename):
    """Generate a dynamic path: property_images/{property_id}/{filename}"""
    return os.path.join('property_images', str(instance.property.id), filename)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=property_image_upload_path)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.title}"
