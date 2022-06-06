from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests as pyreq
from django.views.generic import DetailView
from decouple import config
from .models import City
# Create your views here.


def index(request):

	if request.method == 'POST':
		# TODO: add check if city is unique
		new_city_name = request.POST.get('city', 'unknown city')
		geocoding_url = 'https://api.openweathermap.org/geo/1.0/direct?q={}&appid={}'
		api_response = pyreq.get(geocoding_url.format(new_city_name, config('geocoding_API_KEY'))).json()
		new_city_coords = (api_response[0]['lat'], api_response[0]['lon'])
		new_city = City.objects.create(name=new_city_name, latitude=new_city_coords[0], longitude=new_city_coords[1])
		return HttpResponseRedirect(new_city.get_absolute_url())

	api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
	city_list = City.objects.all()
	weather_list = [pyreq.get(api_url.format(city.name, config('current_API_KEY'))).json() for city in city_list]

	context = {
		'zipper': zip(city_list, weather_list)
	}

	return render(request, 'index.html', context=context)


class CityDetailView(DetailView):
	template_name = 'city_detail.html'
	model = City

	def get_context_data(self, **kwargs):
		context = super(CityDetailView, self).get_context_data(**kwargs)
		api_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'
		context['weather'] = pyreq.get(api_url.format(context['city'].name, config('forecast_API_KEY'))).json()

		# TODO: redo line below it's not working properly
		if not (context['city'].latitude or context['city'].longitude is None):
			context['coords'] = (context['city'].latitude, context['city'].longitude)
		else:
			context['coords'] = None

		return context

	def get_queryset(self):
		return super(CityDetailView, self).get_queryset()
