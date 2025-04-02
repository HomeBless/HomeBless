from django.db import models
from django.contrib.auth.models import User
from .property import Property


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property")


    def __str__(self):
        return f"{self.user.first_name} has {self.property.id} as wishlist."