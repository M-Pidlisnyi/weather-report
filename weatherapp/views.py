from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests as pyreq
from django.views.generic import DetailView
from decouple import config
from .models import City, AppUser
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


def signup(request):

	alert_text = None
	context = {}

	if request.method == 'POST':
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		units = request.POST.get('units')
		if password1 == password2:
			try:
				new_user = User.objects.create_user(username=username, password=password1)
				AppUser.objects.create(user=new_user, units=units)
				login(request, new_user)
				return HttpResponseRedirect('/accounts/profile/')
			except IntegrityError:
				"""integrity error may happen if user with such username already exists"""
				alert_text = "such username already exists\ntry new one or login"
		else:
			alert_text = "passwords don't match"

	if alert_text is not None:
		context['alert'] = alert_text

	return render(request, 'signup.html', context=context)


class CityDetailView(DetailView):
	template_name = 'city_detail.html'
	model = City

	def get_context_data(self, **kwargs):
		context = super(CityDetailView, self).get_context_data(**kwargs)
		api_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'
		context['weather'] = pyreq.get(api_url.format(context['city'].name, config('forecast_API_KEY'))).json()

		return context

	def get_queryset(self):
		return super(CityDetailView, self).get_queryset()

