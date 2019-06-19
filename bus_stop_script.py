import csv
from map.models import BusStop, Test


with open("bus_locations.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        stat_id = row[0]
        name = row[1]
        lat = row[2]
        long = row[3]
        BusStop.objects.create(stat_number=stat_id, name=name, lat=lat, long=long)
'''

with open("test.csv", "r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        col1 = row[0]
        col2 = row[1]
        Test.objects.create(test1 = col1, test2 = col2)
'''
