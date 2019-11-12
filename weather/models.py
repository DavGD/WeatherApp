from django.db import models
from django.core.validators import RegexValidator
import re
# Create your models here.

class CityField(models.Model):
    re_alpha = re.compile('[^\W\d_\s]+$', re.UNICODE)
    alphaletters = RegexValidator(re_alpha, 'Only alpha letters characters are allowed.')
    city = models.CharField(max_length = 25, validators=[alphaletters])

    def __str__(self):
        return self.city
