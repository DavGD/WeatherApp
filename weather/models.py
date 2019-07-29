from django.db import models

# Create your models here.

class CityField(models.Model):
    name = models.CharField(max_length = 25)
