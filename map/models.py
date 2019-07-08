from django.db import models

# Create your models here.
class BusStop(models.Model):

    stop_id = models.IntegerField(primary_key=True, verbose_name='Stop ID')
    stop_name = models.CharField(verbose_name='Bus Station Name', max_length=200)
    lat = models.FloatField(null=True, verbose_name='Latitude')
    lng = models.FloatField(null=True, verbose_name='Longitude')


class RouteStops(models.Model):

    line_id = models.CharField(verbose_name='Line ID', max_length=50)
    route_id = models.ForeignKey('Routes', on_delete=models.CASCADE, verbose_name='Route ID', db_column='route_id')
    stop_id = models.ForeignKey('BusStop', on_delete=models.CASCADE, verbose_name='Stop ID', db_column='stop_id')
    stop_order = models.IntegerField(verbose_name='Stop Order')

    class Meta:
        unique_together = ('route_id', 'stop_id')


class Routes(models.Model):

    route_id = models.CharField(primary_key=True, verbose_name='Route ID', max_length=200)
    start_stop = models.ForeignKey('BusStop', on_delete=models.CASCADE, verbose_name='Start Stop ID', related_name='Start_Stop_ID')
    end_stop = models.ForeignKey('BusStop', on_delete=models.CASCADE, verbose_name='End Stop ID', related_name='End_Stop_ID')
