from django.db import models
from .seller import Seller


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
    construct_year = models.IntegerField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title