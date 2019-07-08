import csv, os, django, sys
from django.shortcuts import get_object_or_404

sys.path.append('../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE','website.settings')
django.setup()

from map.models import BusStop,Route

with open("../csvs/bus_stops.csv", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)
    for row in reader:
        stop_id = int(row[1])
        stop_name = row[2]
        lat = float(row[3])
        lng = float(row[4])
        BusStop.objects.get_or_create(stop_id=stop_id, stop_name=stop_name, lat=lat, lng=lng)

'''
with open("../csvs/routes.csv", "r") as f:
     reader = csv.reader(f, delimiter=',')
     next(reader, None)
     for row in reader:
         routeID = row[0]
         routeName = row[1]
         Routes.objects.get_or_create(routeID=routeID, routeName=routeName)
'''
