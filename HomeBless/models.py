from django.db import models
from django.contrib.auth.models import User
import os


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)    
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    line_id = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    