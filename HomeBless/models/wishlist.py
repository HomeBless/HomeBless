from django.db import models
from .buyer import Buyer
from .property import Property


class Wishlist(models.Model):
    seller = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="buyer")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property")


    def __str__(self):
        return f"{self.seller.first_name} has {self.property.id} as wishlist."
    