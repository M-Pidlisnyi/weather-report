from django.db import models

# Create your models here.


class City(models.Model):
	name = models.CharField(max_length=250, null=False, blank=False)
	longitude = models.FloatField()
	latitude = models.FloatField()

	class Meta:
		verbose_name_plural="Cities"