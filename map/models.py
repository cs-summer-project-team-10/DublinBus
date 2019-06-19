from django.db import models

# Create your models here.
class BusStop(models.Model):

    stat_number = models.IntegerField(unique = True, verbose_name = 'Station ID')
    name = models.CharField('Bus Station Name', max_length = 200)
    lat = models.FloatField(null=True, verbose_name = 'Latitude')
    long = models.FloatField(null=True, verbose_name = 'Longitude')
