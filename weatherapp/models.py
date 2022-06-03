from django.db import models
from django.urls import reverse
# Create your models here.

class City(models.Model):
	name = models.CharField(max_length=250, null=False, blank=False, unique=True)
	longitude = models.FloatField(null=True, blank=True)
	latitude = models.FloatField(null=True, blank=True)

	class Meta:
		verbose_name_plural="Cities"

	def get_absolute_url(self):
		return reverse('city_detail', kwargs={'pk': self.pk})