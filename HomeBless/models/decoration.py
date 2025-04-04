from django.db import models


class Decoration(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
