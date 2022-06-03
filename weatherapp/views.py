from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests as pyreq
from django.views.generic import DetailView

from .models import City
# Create your views here.


def index(request):

	if request.method == 'POST':
		# TODO: add check for unique city
		new_city = City.objects.create(name=request.POST.get('city', 'unknown city'))
		return HttpResponseRedirect(new_city.get_absolute_url())

	api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=e0dfe0214875b7cec701cc3e4b5805ec'
	city_list = City.objects.all()
	weather_list = [pyreq.get(api_url.format(city.name)).json() for city in city_list]

	context = {
		'zipper': zip(city_list, weather_list)
	}

	return render(request, 'index.html', context=context)


class CityDetailView(DetailView):
	template_name = 'city_detail.html'
	model = City

	def get_context_data(self, **kwargs):
		context = super(CityDetailView, self).get_context_data(**kwargs)
		api_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid=c5665be5e701b810ec09c1dcb5a80f68'
		context['weather'] = pyreq.get(api_url.format(context['city'].name)).json()
		return context

	def get_queryset(self):
		return super(CityDetailView, self).get_queryset()
