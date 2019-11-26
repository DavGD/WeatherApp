from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
import requests
from .forms import CityForm
from .models import CityField
from datetime import datetime
import json, random

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
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?id={}&units=metric&appid=8cc2f0a4630ad36fc89c8ab644ef1e28'
    url3 = 'https://api.openweathermap.org/data/2.5//group?id={}&units=metric&appid=8cc2f0a4630ad36fc89c8ab644ef1e28'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('city_site')
    else:
        try:
            city =  CityField.objects.all().last()
            r = requests.get(url.format(city)).json()

            city2 = r['id']
            r2 = requests.get(url2.format(city2)).json()

            time_date_forecast = []
            time_date_forecast_done = []
            for i in range(8):
                time_date_forecast.append(datetime.utcfromtimestamp(r2['list'][i]['dt']+r2['city']['timezone']).strftime('%H:%M:%S, %d.%m.%Y'))
            for x in time_date_forecast:
                time_date_forecast_done.append(x.split(' '))

            list_of_cities = []
            with open(staticfiles_storage.path('city.list.json')) as f:
                data = json.load(f)
                for cit_l in range(len(data)):
                    list_of_cities.append(data[cit_l]['id'])
            r_li = random.sample(list_of_cities, k=5)
            r3 = requests.get(url3.format(r_li).replace(' ', '').replace('[', '').replace(']', '')).json()

            city_weather = {
                'country' : r['sys']['country'],
                'city' : r['name'],
                'temperature' : round(float(r['main']['temp'])),
                'weather' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
                'sunrise' : datetime.utcfromtimestamp(r['sys']['sunrise']+r['timezone']).strftime('%H:%M:%S'),
                'sunset' : datetime.utcfromtimestamp(r['sys']['sunset']+r['timezone']).strftime('%H:%M:%S'),
                'pressure' : int(r['main']['pressure']),
                'humidity' : int(r['main']['humidity']),
                'wind' : round(float(r['wind']['speed']),1),
                'for_time_date' : time_date_forecast_done,
                'for_list' : r2['list'],
                'r_city' : r3['list'],
            }

            context = {'city_weather' : city_weather}

            return render(request, 'weather/details.html', context)

        except KeyError:
            return redirect('main_site')
