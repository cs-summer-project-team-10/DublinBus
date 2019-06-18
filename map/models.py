from django.db import models

# Create your models here.
class Marker(models.Model):
    stat_number = models.IntegerField(null = True, verbose_name = 'Station ID')
    name = models.CharField('Station name', max_length = 120)
    #Right order on creation?
    lat = models.FloatField(null=True, verbose_name = 'latitude')
    long = models.FloatField(null=True, verbose_name = 'latitude')
