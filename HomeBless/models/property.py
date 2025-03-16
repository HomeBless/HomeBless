from django.db import models
from .seller import Seller
from .property_type import PropertyType
from .decoration import Decoration
from .flooring import Flooring
from .wall import Wall
from .ceiling import Ceiling
from .home_feature import HomeFeature
from .project_amenity import ProjectAmenity
from .property_condition import PropertyCondition
from .view import View
from .warranty import Warranty


class Property(models.Model):
    SELLING_TYPE_CHOICES = [
        ('buy', 'For Sale'),
        ('rent', 'For Rent')
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=SELLING_TYPE_CHOICES, default='buy')
    price = models.FloatField(blank=False, null=False)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    floors = models.IntegerField(null=True, blank=True)
    garages = models.IntegerField(null=True, blank=True)
    area = models.FloatField(help_text="Area in square wa")
    is_available = models.BooleanField(default=True)
    construct_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Decoration & Materials
    decoration = models.ForeignKey(Decoration, on_delete=models.SET_NULL, null=True, blank=True)
    flooring = models.ForeignKey(Flooring, on_delete=models.SET_NULL, null=True, blank=True)
    wall_type = models.ForeignKey(Wall, on_delete=models.SET_NULL, null=True, blank=True)
    ceiling_type = models.ForeignKey(Ceiling, on_delete=models.SET_NULL, null=True, blank=True)

    # Features & Amenities (Many-to-Many)
    home_features = models.ManyToManyField(HomeFeature, blank=True)
    project_amenities = models.ManyToManyField(ProjectAmenity, blank=True)

    # Additional Property Conditions
    conditions = models.ManyToManyField(PropertyCondition, blank=True)
    views = models.ManyToManyField(View, blank=True)
    warranties = models.ManyToManyField(Warranty, blank=True)

    # Home Systems (Boolean Fields)
    electrical_system = models.BooleanField(default=True)
    air_conditioning = models.BooleanField(default=False)
    hot_cold_water = models.BooleanField(default=False)
    safety_circuit_breaker = models.BooleanField(default=True)
    backup_power = models.BooleanField(default=False)
    drainage_system = models.BooleanField(default=True)

    def __str__(self):
        return self.title