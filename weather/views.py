from django.shortcuts import render, redirect
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

            temp_forecast = []
            for i in range(8):
                temp_forecast.append(int(r2['list'][i]['main']['temp']))

            icon_forecast = []
            for i in range(8):
                icon_forecast.append(str(r2['list'][i]['weather'][0]['icon']))

            description_forecast = []
            for i in range(8):
                description_forecast.append(str(r2['list'][i]['weather'][0]['description']))

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
                'for_temp' : temp_forecast,
                'for_time_date' : time_date_forecast_done,
                'for_icon' : icon_forecast,
                'for_description' : description_forecast,
            }

            context = {'city_weather' : city_weather}

            return render(request, 'weather/details.html', context)

        except KeyError:
            return redirect('main_site')
