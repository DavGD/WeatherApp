from django.forms import ModelForm
from .models import CityField

class CityForm(ModelForm):

    class Meta:
        model = CityField
        fields = ['city',]
        
