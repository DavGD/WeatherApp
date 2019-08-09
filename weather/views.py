from django.shortcuts import render, redirect
import requests
from .forms import CityForm
from .models import CityField


def main_site(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('city_site')
    else:
        form = CityForm()
        return render(request, 'weather/index.html', {'form':form})

def city_site(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=8cc2f0a4630ad36fc89c8ab644ef1e28'

    try:
        city =  CityField.objects.all().last()

        r = requests.get(url.format(city)).json()

        city_weather = {
            'country' : r['sys']['country'],
            'city' : r['name'],
            'temperature' : r['main']['temp'],
            'weather' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        context = {'city_weather' : city_weather}

        return render(request, 'weather/details.html', context)

    except KeyError:
        return redirect('main_site')
