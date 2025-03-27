from django.db import models
from django.contrib.auth.models import User


def buyer_profile_picture_upload_path(instance, filename):
    return f"buyer_profiles/{instance.id}/{filename}"


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    line_id = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=buyer_profile_picture_upload_path, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name