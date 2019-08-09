from django.db import models

# Create your models here.

class CityField(models.Model):
    city = models.CharField(max_length = 25)

    def __str__(self):
        return self.city
