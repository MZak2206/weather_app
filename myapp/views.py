import locale
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import requests
from babel.dates import format_date, format_datetime, format_time
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib import dates as mpl_dates
from matplotlib.ticker import FuncFormatter
import matplotlib
matplotlib.use('Agg')

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
        dates = []
        temperatures = []
        
        today = datetime.now().date()
        for i in range(5):
            date = today + timedelta(days=i)
            weather_info = {
                "city": city,
                "day": date,
                "weather_description" : data["list"][i]["weather"][0]["description"],
                "temperature" : data["list"][i]["main"]["temp"],
                "humidity" : data["list"][i]["main"]["humidity"],
                "icon" : data["list"][i]["weather"][0]["icon"]
            }
            weather_data.append(weather_info)
            
            dates.append(date)
            temperatures.append(weather_info["temperature"])
            
        plt.plot(dates, temperatures)
        plt.xlabel('Data')
        plt.ylabel('Temperatura (°C)')
        plt.title('Wykres temperatury')
        
        # Formatowanie osi czasu
        def get_weekday(x, pos=None):
            
            date =  format_date(dates[pos], format='d/M/yyyy', locale='pl_PL')
            weekday =  format_date(dates[pos], format='EEEE', locale='pl_PL')
            return str(date+"\n"+weekday)
        
        plt.gca().xaxis.set_major_formatter(FuncFormatter(get_weekday))
        plt.gca().xaxis.set_major_locator(mpl_dates.DayLocator())
        plt.gcf().autofmt_xdate()  # Automatyczne dostosowanie etykiet osi X

        
        plt.tight_layout()  # Opcjonalne - poprawia układ wykresu

        plt.savefig('static/wykres.png')  # Zapisz wykres do pliku (opcjonalnie)
        plt.close()  # Zamknij wykres, aby zwolnić pamięć
        
        return weather_data
    else:
        return []
