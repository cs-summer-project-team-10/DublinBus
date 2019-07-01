from django.db import models

# Create your models here.
class BusStop(models.Model):

    stat_number = models.IntegerField(primary_key=True, verbose_name = 'Station ID')
    name = models.CharField(verbose_name='Bus Station Name', max_length = 200)
    lat = models.FloatField(null=True, verbose_name = 'Latitude')
    lng = models.FloatField(null=True, verbose_name = 'Longitude')


class Vehicle(models.Model):

    DataSource = models.CharField( verbose_name = 'Unique Bus Operator Code',max_length=50)
    DayOfService = models.CharField(verbose_name='Day of service',max_length=100)
    VehicleID = models.CharField(verbose_name='Unique vehicle code arriving at this stop point', max_length=50)
    Distance = models.IntegerField(verbose_name='Distance travelled by the vehicle in this day')
    Minutes = models.IntegerField(verbose_name='Time worked by the vehicle in the corresponding day')
    LastUpdate = models.CharField(verbose_name='Time of the last record update',max_length=100)
    Note = models.CharField(verbose_name='Free note',max_length=255)



class Trip(models.Model):

    DataSource = models.CharField( verbose_name = 'Unique Bus Operator Code',max_length=50)
    DayOfService = models.CharField(verbose_name='Day of service,One day of service could last more than 24 hours',max_length=100)
    TripID = models.CharField(verbose_name='Unique trip code', max_length=50)
    LineID = models.CharField(verbose_name='Unique line code', max_length=50)
    RouteID = models.CharField(verbose_name='Unique route code', max_length=50)
    Direction = models.CharField(verbose_name='Route direction:IB or OB', max_length=10)
    PlannedTime_Dep = models.IntegerField(verbose_name='Planned departure time of the trip, in seconds')
    PlannedTime_Arr= models.IntegerField(verbose_name='Planned arrival time of the trip, in seconds')
    Basin = models.CharField(verbose_name='Basin code', max_length=50)
    TenderLot = models.CharField(verbose_name='Tender lot', max_length=50)
    ActualTime_Dep = models.IntegerField(verbose_name='Actual departure time of the trip, in seconds')
    ActualTime_Arr = models.IntegerField(verbose_name='Actual arrival time of the trip, in seconds')
    Suppressed = models.IntegerField(verbose_name='The whole trip has been suppressed (0 =achieved, 1 = suppressed)')
    JustificationID = models.IntegerField(verbose_name='Fault code')
    LastUpdate = models.CharField(verbose_name='Time of the last record update',max_length=100)
    Note = models.CharField(verbose_name='Free note',max_length=255)





class LeaveTime(models.Model):

    DataSource = models.CharField( verbose_name = 'Unique Bus Operator Code',max_length=50)
    DayOfService = models.CharField(verbose_name='Day of service,One day of service could last more than 24 hours',max_length=100)
    TripID = models.CharField(verbose_name='Unique trip code', max_length=50)
    ProgrNumber = models.IntegerField(verbose_name='Sequential position of the stop point in the trip')
    StopPointID = models.CharField(verbose_name='Unique stop point code', max_length=50)
    PlannedTime_Dep = models.IntegerField(verbose_name='Planned departure time from the stop point, in seconds')
    PlannedTime_Arr= models.IntegerField(verbose_name='Planned arrival time at the stop point, in seconds')
    ActualTime_Dep = models.IntegerField(verbose_name='Actual departure time from the stop point, in seconds')
    ActualTime_Arr = models.IntegerField(verbose_name='Actual arrival time at the stop point, in seconds')
    VehicleID = models.CharField(verbose_name='Unique vehicle code arriving at this stop point', max_length=50)
    Passengers = models.IntegerField(verbose_name='Number of passengers on board (previous link)')
    PassengersIn = models.IntegerField(verbose_name='Number of boarded passengers')
    PassengersOut = models.IntegerField(verbose_name='Number of descended passengers')
    Distance = models.IntegerField(verbose_name='Distance measured from the beginning of the trip')
    Suppressed = models.IntegerField(verbose_name='The whole trip has been partially suppressed (0 =achieved, 1 = suppressed)')
    JustificationID = models.IntegerField(verbose_name='Fault code')
    LastUpdate = models.CharField(verbose_name='Time of the last record update',max_length=100)
    Note = models.CharField(verbose_name='Free note',max_length=255)







class TrackingRawData(models.Model):

    DataSource = models.CharField(verbose_name = 'Unique Bus Operator Code',max_length=50)
    DayOfService = models.CharField(verbose_name='Day of service,One day of service could last more than 24 hours',max_length=100)
    VehicleID = models.CharField(verbose_name='Unique vehicle code', max_length=50)
    TimePos = models.CharField(verbose_name='Time of the tracking',max_length=100)
    TripID = models.CharField(verbose_name='Unique trip code', max_length=50)
    PosX = models.IntegerField(verbose_name='Longitude')
    PosY = models.IntegerField(verbose_name='Latitude')
    Odometer = models.IntegerField(verbose_name='Odometer of the vehicle')
    TripOdometer = models.IntegerField(verbose_name='Odometer for the trip')
    PassengersIn = models.IntegerField(verbose_name='Number of boarded passengers')
    PassengersOut = models.IntegerField(verbose_name='Number of descended passengers')



class Justification(models.Model):

    DataSource = models.CharField(primary_key=True, verbose_name = 'Unique Bus Operator Code',max_length=50)
    JustificationID = models.IntegerField(verbose_name='Unique Variation Code')



class RouteStops(models.Model):

    routeID= models.ForeignKey( 'Routes', on_delete=models.CASCADE)

    # routeID = models.IntegerField(verbose_name='Route ID')
    # stopID = models.IntegerField(verbose_name='Route Name', max_length=50)

    stopID = models.ForeignKey( 'BusStop', on_delete=models.CASCADE)

    stop_order =models.IntegerField(verbose_name='Route Name')

class Routes(models.Model):

    routeID  = models.IntegerField(verbose_name='Route ID', primary_key=True)

    routeName = models.CharField(verbose_name='Route Name', max_length=50)








