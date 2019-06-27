from django.db import models

# Create your models here.
class BusStop(models.Model):

    stat_number = models.IntegerField(primary_key = True, verbose_name = 'Station ID')
    name = models.CharField('Bus Station Name', max_length = 200)
    lat = models.FloatField(null=True, verbose_name = 'Latitude')
    lng = models.FloatField(null=True, verbose_name = 'Longitude')
