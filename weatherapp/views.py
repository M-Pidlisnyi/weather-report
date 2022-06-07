from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests as pyreq
from django.views.generic import DetailView
from decouple import config
from .models import City


# Create your views here.


def index(request):

	if request.method == 'POST':
		# TODO: add checkbox for adding city to DB
		new_city_name = request.POST.get('city', 'unknown city')

		geocoding_url = 'https://api.openweathermap.org/geo/1.0/direct?q={}&appid={}'
		api_response = pyreq.get(geocoding_url.format(new_city_name, config('geocoding_API_KEY'))).json()
		new_city_coords = (api_response[0]['lat'], api_response[0]['lon'])

		try:
			new_city = City.objects.create(name=new_city_name, latitude=new_city_coords[0], longitude=new_city_coords[1])
		except IntegrityError:
			"""integrity error may happen if city with such a name already is in db """
			new_city = City.objects.get(name=new_city_name)
		return HttpResponseRedirect(new_city.get_absolute_url())

	api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
	city_list = City.objects.all()
	weather_list = [pyreq.get(api_url.format(city.name, config('current_API_KEY'))).json() for city in city_list]

	context = {
		'zipper': zip(city_list, weather_list)
	}

	return render(request, 'index.html', context=context)


def user_profile(request, username):

	return render(request, 'user_profile.html')


class CityDetailView(DetailView):
	template_name = 'city_detail.html'
	model = City

	def get_context_data(self, **kwargs):
		context = super(CityDetailView, self).get_context_data(**kwargs)
		api_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'
		context['weather'] = pyreq.get(api_url.format(context['city'].name, config('forecast_API_KEY'))).json()

		# check if coords for city are available
		# not sure if i need to check at all
		if not (context['city'].latitude or context['city'].longitude is None):
			context['coords'] = (context['city'].latitude, context['city'].longitude)
		else:
			context['coords'] = None

		return context

	def get_queryset(self):
		return super(CityDetailView, self).get_queryset()

