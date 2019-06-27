import csv
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','website.settings')

import django
django.setup()

from map.models import BusStop

with open("bus_locations.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        stat_id = row[0]
        name = row[1]
        lat = row[2]
        lng = row[3]
        BusStop.objects.get_or_create(stat_number=stat_id, name=name, lat=lat, lng=lng)
