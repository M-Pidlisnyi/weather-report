from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests as pyreq
from .models import City
# Create your views here.


def index(request):

	if request.method == 'POST':
		new_city = City.objects.create(name=request.POST.get('city', 'unknown city'))
		return HttpResponseRedirect('/')

	api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=e0dfe0214875b7cec701cc3e4b5805ec'
	city_list = City.objects.all()
	weather_list = [pyreq.get(api_url.format(city.name)).json() for city in city_list]

	context = {
		'zipper': zip(city_list, weather_list)
	}

	return render(request, 'index.html', context=context)
