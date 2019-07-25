from django import forms
from .models import CityField

class CityForm(forms.ModelForm):

    class Meta:
        model = CityField
        fields = ('name',)
