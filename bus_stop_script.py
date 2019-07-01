import csv
import os
from django.shortcuts import get_object_or_404

os.environ.setdefault('DJANGO_SETTINGS_MODULE','website.settings')

import django
django.setup()

from map.models import BusStop,RouteStops,Routes,LeaveTime,Trip,Vehicle,TrackingRawData,Justification

with open("bus_locations.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        stat_id = row[0]
        name = row[1]
        lat = row[2]
        lng = row[3]
        BusStop.objects.get_or_create(stat_number=stat_id, name=name, lat=lat, long=lng)


with open("Routes.csv", "r") as f:
     reader = csv.reader(f, delimiter=',')
     next(reader, None)
     for row in reader:
         routeID = row[0]
         routeName = row[1]
         Routes.objects.get_or_create(routeID=routeID, routeName=routeName)


with open("rt_leavetimes_2017_I_DB_1000.txt", "r") as f:
    reader = csv.reader(f, delimiter=';')
    next(reader, None)
    for row in reader:
         datasource = row[0]
         dayofservice = row[1]
         tripid = row[2]
         progrnumber = row[3]
         stoppointid = row[4]
         plannedtime_arr = row[5]
         plannedtime_dep = row[6]
         actualtime_arr= row[7]
         actualtime_dep = row[8]
         vehicleid = row[9]
         # passengers = row[10]
         passengers = 1
         # passengersin = row[11]
         passengersin = 1
         # passengersout = row[12]
         passengersout =1
         # distance = row[13]
         # suppressed = row[14]
         distance = 1
         suppressed = 1
         # justificationid = row[15]
         justificationid = 1
         lastupdate = row[16]
         note = row[17]
         LeaveTime.objects.get_or_create(DataSource=datasource,DayOfService=dayofservice,TripID =tripid,ProgrNumber=progrnumber,
                                      StopPointID=stoppointid,PlannedTime_Arr=plannedtime_arr,PlannedTime_Dep=plannedtime_dep,
                                      ActualTime_Arr=actualtime_arr,ActualTime_Dep=actualtime_dep,VehicleID=vehicleid,Passengers=passengers,
                                      PassengersIn=passengersin,PassengersOut=passengersout, Distance=distance,Suppressed =suppressed,
                                      JustificationID=justificationid,LastUpdate =lastupdate, Note=note)


# Check column order
with open("rt_trips_2017_I_DB_1000.txt", "r") as f:
    reader = csv.reader(f, delimiter=';')
    next(reader, None)
    for row in reader:
         datasource = row[0]
         dayofservice = row[1]
         tripid = row[2]
         lineid = row[3]
         routeid = row[4]
         direction= row[5]
         plannedtime_arr = row[6]
         plannedtime_dep = row[7]
         actualtime_arr = row[8]
         actualtime_dep = row[9]
         basin = row[10]
         # tenderlot = row[11]
         # suppressed = row[12]
         # justificationid = row[13]
         tenderlot = 1
         suppressed = 1
         justificationid =1
         lastupdate = row[14]
         note = row[15]
         Trip.objects.get_or_create(Datasource=datasource, Dayofservice=dayofservice, TripID=tripid,LineID =lineid,
                                    RouteID=routeid, Direction=direction, PlannedTime_Arr=plannedtime_arr,
                                    PlannedTime_Dep=plannedtime_dep,ActualTime_Arr=actualtime_arr, ActualTime_Dep=actualtime_dep,
                                    Basin =basin, TenderLot=tenderlot,Suppressed=suppressed, JustificationID=justificationid,
                                    LastUpdate=lastupdate,Note=note)


# Check column order
with open("rt_Vehicle.txt", "r") as f:
    reader = csv.reader(f, delimiter=';')
    next(reader, None)
    for row in reader:
        datasource = row[0]
        dayofservice = row[1]
        vehicleid  = row[2]
        distance = row[3]
        minutes = row[4]
        lastupdate = row[5]
        note = row[6]
        Trip.objects.get_or_create(Datasource=datasource, Dayofservice=dayofservice,
                                VehicleID=vehicleid, Distance=distance,Minutes=minutes,
                                Lastupdate=lastupdate, Note=note)
