from django.shortcuts import render
import requests as pyreq
# Create your views here.


def index(request):
	api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=e0dfe0214875b7cec701cc3e4b5805ec'

	city_name = 'Kalush'

	weather = [pyreq.get(api_url.format(city_name)).json()]

	context = {
		'city': city_name,
		'weather': weather[0]
	}

	return render(request, 'index.html', context=context)
