import csv, os, django, sys
from django.shortcuts import get_object_or_404

sys.path.append('../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE','website.settings')
django.setup()

from map.models import BusStop,Routes

with open("../csvs/bus_locations.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        stat_id = row[0]
        name = row[1]
        lat = row[2]
        lng = row[3]
        BusStop.objects.get_or_create(stat_number=stat_id, name=name, lat=lat, lng=lng)


with open("../csvs/routes.csv", "r") as f:
     reader = csv.reader(f, delimiter=',')
     next(reader, None)
     for row in reader:
         routeID = row[0]
         routeName = row[1]
         Routes.objects.get_or_create(routeID=routeID, routeName=routeName)
