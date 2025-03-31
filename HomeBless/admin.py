from django.contrib import admin
from .models import Seller, Property, PropertyImage

# Register your models here.
admin.site.register(Seller)
admin.site.register(Property)
admin.site.register(PropertyImage)
