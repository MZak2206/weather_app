# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import datetime, timedelta
import locale


def weather(request):
    city = "Łódź"
    if request.method == "POST":
        city = request.POST.get("city", "Łódź")
    return render(request, 'weather.html', {'data': get_weather_data(city)})


def get_weather_data(city):
    api_key = "5acd2a90879682f6a0023ad1a75ff7df"    
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&lang=pl&units=metric"
    
    
    response = requests.get(url)

    locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')
    if response.status_code == 200:
        data = response.json()
        weather_data = []
        today = datetime.now().date()
        for i in range(5):
            date = today + timedelta(days=i)
            # day = date.strftime("%A")
            # print(day)
            weather_info = {
                "city": city,
                "day": date,
                "weather_description" : data["list"][i]["weather"][0]["description"],
                "temperature" : data["list"][i]["main"]["temp"],
                "humidity" : data["list"][i]["main"]["humidity"],
                "icon" : data["list"][i]["weather"][0]["icon"]
            }
            weather_data.append(weather_info)
        return weather_data
    else:
        return []
