from django.shortcuts import render, redirect
import requests
from .forms import CityForm
from .models import CityField
from datetime import datetime


def main_site(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('city_site')
    else:
        lastest = CityField.objects.values_list('city', flat=True).order_by('-id')[:10]
        last_search = []
        for i in lastest:
            if i not in last_search:
                last_search.append(i)

        con_site = {
            'form' : CityForm(),
            'last_five' : last_search[:5],
        }

        return render(request, 'weather/main.html', {'con_site': con_site})

def city_site(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8cc2f0a4630ad36fc89c8ab644ef1e28'

    try:
        city =  CityField.objects.all().last()

        r = requests.get(url.format(city)).json()

        city_weather = {
            'country' : r['sys']['country'],
            'city' : r['name'],
            'temperature' : int(r['main']['temp']),
            'weather' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'sunrise' : datetime.utcfromtimestamp(r['sys']['sunrise']+r['timezone']).strftime('%H:%M:%S'),
            'sunset' : datetime.utcfromtimestamp(r['sys']['sunset']+r['timezone']).strftime('%H:%M:%S'),
        }

        context = {'city_weather' : city_weather}

        return render(request, 'weather/details.html', context)

    except KeyError:
        return redirect('main_site')
