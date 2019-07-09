import csv, os, django, sys
from django.shortcuts import get_object_or_404

sys.path.append('../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE','website.settings')
django.setup()

from map.models import BusStop,RouteStops, Route

with open("../csvs/bus_stops.csv", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)
    for row in reader:
        stop_id = int(row[1])
        stop_name = row[2]
        lat = float(row[3])
        lng = float(row[4])
        BusStop.objects.get_or_create(stop_id=stop_id, stop_name=stop_name, lat=lat, lng=lng)


with open("../csvs/route_stops.csv", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)
    #count = 0
    # error_set_stops = set([])
    # error_set_routes = set([])

    for row in reader:
        line_id = row[0]
        route_id = row[1]
        stop_id = row[2]
        stop_order = row[3]

        start_stop = BusStop.objects.get(stop_id = 131)
        end_stop = BusStop.objects.get(stop_id = 131)

        #Must change at later date
        Route.objects.get_or_create(route_id=route_id, start_stop= start_stop, end_stop=end_stop)

        try:
            route =  Route.objects.get(route_id = route_id)
            stop = BusStop.objects.get(stop_id = stop_id)
            #print(stop)
            RouteStops.objects.get_or_create(line_id=line_id, route_id=route, stop_id=stop, stop_order=stop_order)


        except:
            pass
            #error_set_stops.add(stop_id)
            #error_set_routes.add(row[1])
            #count+=1
'''
    print(count)

    with open('errors.txt', 'w') as f:
        for item in error_set_stops:
            f.write(str(item)+ " ")
        f.write("\nRoutes Below\n")
        for item in error_set_routes:
            f.write(str(item) + " ")
'''
