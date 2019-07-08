import csv, os, django, sys
from django.shortcuts import get_object_or_404

sys.path.append('../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE','website.settings')
django.setup()

from map.models import RouteStops, Routes, BusStop

with open("../csvs/route_stops.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    next(reader, None)
    for row in reader:
        routeID1 = row[0]
        stopID1 = row[1]
        stop_order1 = row[2]
        RouteStops.objects.get_or_create(routeID=Routes.objects.get(routeID=routeID1), stopID=BusStop.objects.get(stat_number=stopID1), stop_order=stop_order1)
