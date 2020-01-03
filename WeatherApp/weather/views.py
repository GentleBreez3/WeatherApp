from django.shortcuts import render,redirect
import requests
from weather.models import City
from weather.forms import CityForm
# Create your views here.

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=289eaa033a39781f2a8c9a7014611343"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'id' : city.id,
            "city": city.name,
            "temparature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
        }
        weather_data.append(city_weather)

    context = {"weather_data": weather_data, "form":form}

    return render(request, "weather/weather.html", context)
    
def delete(request, id):

    if request.method == 'POST':
        City.objects.filter(id=id).delete()

    return redirect('/')
