from django.shortcuts import render, redirect
import requests
from .forms import CityForm
from .models import CityField

def main_site(request):
    if request.method == 'POST':
        form = CityForm()
        if form.is_valid():
            form.save()
            return redirect('city_site', pk=form.pk)
    else:
        form = CityForm()
        return render(request, 'weather/index.html', {'form':form})
