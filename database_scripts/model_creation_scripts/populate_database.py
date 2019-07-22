import csv, os, django, sys
from django.shortcuts import get_object_or_404
sys.path.append('../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE','website.settings')
django.setup()

from map.models import Routes, Stops, Shapes, CalendarService, CalendarExceptions, Trips


def change_date_format(date):
   '''
    Simple function that inserts '-' between YYYY MM DD
'''

    new_date = date[:4] + "-" + date[4:6] + "-" + date[6:]

    return new_date

def change_stop_id(stop_id):
    '''
    Function that changes stop ids to a shortened version
    '''

    exception_dict = {
        "gen:57102:7730:0:1" : "8240DB007682",
        "gen:57102:7732:0:1" : "8240DB007676",
        "gen:57102:7743:0:1" : "8240DB007690",
        "gen:57102:7943:0:1" : "8240DB007703",
        "gen:57102:7731:0:1" : "8240DB007674",
        "gen:57102:7733:0:1" : "8240DB007677",
        "gen:57102:7948:0:1" : "8240DB007701"
    }

    try:
        short_stop_id = int(stop_id[6:])

    except ValueError:
        try:
            s = stop_id.split("_")[0]
            short_stop_id = int(s[6:])

        except ValueError:
            #print(stop_id)
            dict_value = exception_dict[stop_id]
            short_stop_id = change_stop_id(dict_value)
            #print(short_stop_id)

    return short_stop_id


with open("../csvs/routes.txt", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)

    for row in reader:
        route_id = row[1]
        agency_id = row[4]
        route_short_name = row[7]

        Routes.objects.get_or_create(route_id = route_id, agency_id = agency_id, route_short_name = route_short_name)


with open("../csvs/stops.txt", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)

    for row in reader:
        try:
            stop_id_short = change_stop_id(row[3])
        except:
            stop_id_short = 666666
            continue

        stop_id = row[3]
        stop_name = row[4]
        stop_lat = row[0]
        stop_lng = row[2]

        Stops.objects.get_or_create(stop_id = stop_id, stop_id_short = stop_id_short, stop_name = stop_name, stop_lat = stop_lat, stop_lng = stop_lng)

with open("../csvs/calendar.txt", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)

    for row in reader:
        service_id = row[0]
        start_date = change_date_format(row[1])
        end_date = change_date_format(row[2])

        CalendarService.objects.get_or_create(service_id = service_id, start_date = start_date, end_date = end_date, \
                                            monday = row[3], tuesday = row[4], wednesday = row[5], thursday = row[6], \
                                            friday = row[7], saturday = row[8], sunday = row[9])


with open("../csvs/calendar_dates.txt", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)

    for row in reader:
        service_id = row[0]
        service_id = CalendarService.objects.get(service_id = service_id)
        exception_date = change_date_format(row[1])
        exception_type = row[2]

        CalendarExceptions.objects.get_or_create(service_id = service_id, exception_date = exception_date, exception_type = exception_type)

with open("../csvs/shapes.txt", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)

    for row in reader:
        shape_id = row[0]
        shape_point_lat = row[1]
        shape_point_lng = row[2]
        shape_point_sequence = row[3]
        shape_dist_travelled = row[4]

        Shapes.objects.get_or_create(shape_id = shape_id, shape_point_lat = shape_point_lat, shape_point_lng = shape_point_lng, shape_point_sequence = shape_point_sequence, shape_dist_travelled = shape_dist_travelled)


with open("../csvs/trips.txt", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)

    for row in reader:

        trip_id = row[5]
        route_id = Routes.objects.get(route_id = row[0])
        direction = row[1]
        trip_headsign = row[2]
        shape_id = row[3]
        service_id = CalendarService.objects.get(service_id = row[4])
       # print(trip_id,route_id,direction,trip_headsign,shape_id,service_id)

        Trips.objects.get_or_create(trip_id = trip_id, route_id = route_id, direction = direction, trip_headsign = trip_headsign, shape_id = shape_id, service_id = service_id)


'''
Used to create models using SQL to speed up process
'''



from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy

engine = create_engine('postgresql+psycopg2://stephen:1993@127.0.0.1:5432/new_models')

#data = pd.read_csv("../csvs/shapes.txt")
#data.to_sql('test', engine, if_exists = 'append', chunksize = 1000)

data = pd.read_csv("../csvs/stop_times.txt")

data = data[['trip_id', 'stop_id', 'stop_sequence', 'arrival_time', 'departure_time', 'stop_headsign', 'shape_dist_traveled']]

data.to_sql(name = 'map_trip_stop_times', con = engine, if_exists = 'append', chunksize = 1000, index = False, \
            dtype = {"trip_id" : sqlalchemy.types.VARCHAR(length=100),
                    "stop_id" : sqlalchemy.types.VARCHAR(length=100),
                    "stop_sequence" : sqlalchemy.types.INTEGER(),
                    "scheduled_arrival_time" : sqlalchemy.DateTime(),
                    "scheduled_dept_time" : sqlalchemy.DateTime(),
                    "stop_headsign" : sqlalchemy.types.VARCHAR(length=200),
                    "distance_travelled" : sqlalchemy.types.VARCHAR(length=200)})

'''
# Old long way of creating models
'''
'''
with open("../csvs/stop_times.txt", "r") as read_file:
    reader = csv.reader(read_file, delimiter=',')
    next(reader, None)

    bulk_list = []

    for row in reader:
        trip_id = Trips.objects.get(trip_id = row[0])
        stop_id = Stops.objects.get(stop_id = row[3])
        scheduled_arrival_time = row[1]
        scheduled_dept_time = row[2]
        stop_sequence = row[4]
        stop_headsign = row[5]
        distance_travelled = str(row[8])

        bulk_list.append(StopTripTimes(trip_id = trip_id, stop_id = stop_id, scheduled_arrival_time = scheduled_arrival_time, scheduled_dept_time = scheduled_dept_time, stop_sequence = stop_sequence, stop_headsign = stop_headsign, distance_travelled = distance_travelled))

    print("Finished making list")

    StopTripTimes.objects.bulk_create(bulk_list)

        #StopTripTimes.get_or_create(trip_id = trip_id, stop_id = stop_id, scheduled_arrival_time = scheduled_arrival_time, scheduled_dept_time = scheduled_dept_time, stop_sequence = stop_sequence, stop_headsign = stop_headsign, distance_travelled = distance_travelled)
'''
