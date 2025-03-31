from django.db import models
from .seller import Seller
from .property_type import PropertyType
from .decoration import Decoration
from .flooring import Flooring
from .wall import Wall
from .ceiling import Ceiling
from .home_feature import HomeFeature
from .property_condition import PropertyCondition
from .view import View
from .warranty import Warranty
from .home_system import HomeSystem
from .security import Security
from .common_area import CommonArea
from .facility import Facility
from .travelling import Travelling


class Property(models.Model):
    SELLING_TYPE_CHOICES = [
        ('buy', 'For Sale'),
        ('rent', 'For Rent')
    ]
    SELLER_STATUS_CHOICES = [
        ('owner', 'Owner'),
        ('agent', 'Agent')
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255)
    description = models.TextField()
    seller_status = models.CharField(max_length=10, choices=SELLER_STATUS_CHOICES, default='owner')
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)
    selling_type = models.CharField(max_length=10, choices=SELLING_TYPE_CHOICES, default='buy')
    price = models.FloatField(blank=True, null=True)
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

    # Decoration & Materials
    decoration = models.ManyToManyField(Decoration, blank=True)
    flooring = models.ManyToManyField(Flooring, blank=True)
    wall_type = models.ManyToManyField(Wall, blank=True)
    ceiling_type = models.ManyToManyField(Ceiling, blank=True)

    # Features & Amenities (Many-to-Many)
    home_features = models.ManyToManyField(HomeFeature, blank=True)
    security = models.ManyToManyField(Security, blank=True)
    common_area = models.ManyToManyField(CommonArea, blank=True)
    travelling = models.ManyToManyField(Travelling, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)

    # Additional Property Conditions
    conditions = models.ManyToManyField(PropertyCondition, blank=True)
    views = models.ManyToManyField(View, blank=True)
    warranties = models.ManyToManyField(Warranty, blank=True)

    # Home Systems
    home_systems = models.ManyToManyField(HomeSystem, blank=True)

    # Contacts
    line_id = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.title
