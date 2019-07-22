
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, render, redirect
import json
import requests
import datetime
import pickle
import pandas as pd

from datetime import date

from .models import MapTripStopTimes, Stops, CalendarService, Trips, Routes, Shapes


def home_page(request):
    ''' Simple view that renders the index html template with all the bus stop information
        using Jinja2
    '''
    bus_stops = Stops.objects.all()
    bus_stop_list = []
    for bus_stop in bus_stops:
        bus_stop_list.append((bus_stop.stop_id, bus_stop.stop_id_short, bus_stop.stop_name, bus_stop.stop_lat, bus_stop.stop_lng))

    return render(request, 'map/index.html', {'JSONdata': json.dumps(bus_stop_list)})



def return_routes(request):
    '''
    Function that checks for common bus routes between two stops provided by user.
    Initially will check between two stops provided and in time will check also common
    bus stops between routes servicing these stops.

    It will then call a predictive model on this route per stop etc.
    '''

    #start_stop = request.GET['startstop']
    #dest_stop = request.GET['endstop']
    #time_specified = request.GET['time_specified']
    #date_specified = request.GET['date_specified']

    #Get weather
    #response = requests.get("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0927fd5dff272fdbd486187e54283310")
    #weather_data = json.loads(response.content.decode('utf-8'))
    #print(weather_data)
    weather = "dummy"

    # Convert time to time period
    # if seconds >= 0 and seconds < 25200:
    #     return 0
    # elif seconds >= 25200 and seconds < 36000:
    #     return 5
    # elif seconds >= 36000 and seconds < 54000:
    #     return 3
    # elif seconds >= 54000 and seconds < 61200:
    #     return 4
    # elif seconds >= 61200 and seconds < 68400:
    #     return 6
    # elif seconds >= 68400 and seconds < 79200:
    #     return 2
    # elif seconds >= 79200:
    #     return 1

    time_period =  "dummy"

    # Convert date to week or weekend

    start_stop = "8220DB001069"
    dest_stop = "8220DB000670"

    start_stop = 1069
    dest_stop = 670

    start_stop = Stops.objects.get(stop_id_short = start_stop)
    dest_stop = Stops.objects.get(stop_id_short = dest_stop)

    date_time = datetime.datetime.now()
    time = datetime.datetime.now().strftime('%H:%M:%S')
    todays_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Monday is 0
    day = datetime.datetime.today().weekday()

    time_range1 = (datetime.datetime.now() + datetime.timedelta(minutes=80)).strftime('%H:%M:%S')
    time_range2 = (datetime.datetime.now() + datetime.timedelta(minutes=60)).strftime('%H:%M:%S')

    #print(start_stop, dest_stop, time, time_range1, time_range2, todays_date, day)

    #Get service IDs for todays dates
    if day == 0:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = todays_date, end_date__gte = todays_date, monday = True))
        weekday = True
    elif day == 1:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = todays_date, end_date__gte = todays_date, tuesday = True))
        weekday = True
    elif day == 2:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = todays_date, end_date__gte = todays_date, wednesday = True))
        weekday = True
    elif day == 3:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = todays_date, end_date__gte = todays_date, thursday = True))
        weekday = True
    elif day == 4:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = todays_date, end_date__gte = todays_date, friday = True))
        weekday = True
    elif day == 5:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = todays_date, end_date__gte = todays_date, saturday = True))
        weekday = False
    elif day == 6:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = todays_date, end_date__gte = todays_date, sunday = True))
        weekday = False

    #print(service_list)
    #tuple
    #print((service_list)[0][0])

    # Get all trips of starting bus stop that are within a time range given either side of what user specified
    trip_id_list = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(stop_id = start_stop, arrival_time__range = (time_range2, time_range1)))

    #print(trip_id_list)
    #print(len(trip_id_list))

    # Narrow the trips to those that have service on todays date
    valid_trip_id_list = list(Trips.objects.values_list('trip_id', flat = True).filter(trip_id__in = trip_id_list, service_id__in = service_list))

    #print(valid_trip_id_list)
    #print(len(valid_trip_id_list))
    #for trip in trip_id_list:
    #    valid_trip_id_list.append(trip)


    # Get trips that are also specfic to destiantion stop
    common_trip_id_list = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(trip_id__in = valid_trip_id_list, stop_id = dest_stop))
    #print(common_trip_id_list)
    #print("Common trips:",len(common_trip_id_list))

    # Create dictionary of routes possible between stops
    temp_route_dict = {}
    data = []

    for trip in common_trip_id_list:
        route_dict = {}

        #print(trip)
        trips_query_set = Trips.objects.filter(trip_id = trip).values_list('route_id', 'trip_headsign', 'shape_id')

        route_id = trips_query_set[0][0]
        trip_headsign = trips_query_set[0][1]
        shape_id = trips_query_set[0][2]
        #print(trips_query_set)
        #print(route_id, trip_headsign, shape_id)
        route_short_name = Routes.objects.filter(route_id = route_id).values_list('route_short_name', flat = True)[0]
        #print(route_short_name)

        # Create a direct route object that holds all the details for this route
        # Pass weather, time period etc in here
        temp_route_dict[trip] = DirectRoute(weather, weekday, time_period, start_stop, dest_stop, trip, route_id, route_short_name, trip_headsign, shape_id)

        route_dict["route_id"] = temp_route_dict[trip].route_id
        route_dict["trip_id"] = temp_route_dict[trip].trip_id
        route_dict["route_short_name"] = temp_route_dict[trip].route_short_name
        route_dict["trip_headsign"] = temp_route_dict[trip].trip_headsign
        route_dict["start_stop_id"] = temp_route_dict[trip].start_stop_id
        route_dict["dest_stop_id"] = temp_route_dict[trip].dest_stop_id
        route_dict["start_stop_id_short"] = temp_route_dict[trip].start_stop_id_short
        route_dict["dest_stop_id_short"] = temp_route_dict[trip].dest_stop_id_short
        route_dict["number_stops"] = temp_route_dict[trip].number_stops
        route_dict["departure_time"] = temp_route_dict[trip].departure_time
        route_dict["all_stops_list"] = temp_route_dict[trip].all_stops_list
        route_dict["subroute_stops_list"] = temp_route_dict[trip].subroute_stops_list
        route_dict["route_shape_points"] = temp_route_dict[trip].route_shape_points
        route_dict["subroute_shape_points"] = temp_route_dict[trip].subroute_shape_points


        data.append(route_dict)

    if len(data) == 0:
        print("No common route found")
        multi_routing(weather, weekday, time_period, valid_trip_id_list, start_stop, dest_stop, time_range1, time_range2, service_list)
        # Call multi-routing API
    return JsonResponse({'routes_data': data})



def multi_routing(weather, weekday, time_period, start_stop_valid_trip_id_list, start_stop, dest_stop, time_range1, time_range2, service_list):
    #start_stop = start_stop
    #dest_stop = dest_stop

    start_stop_valid_trips = start_stop_valid_trip_id_list
    print(start_stop, dest_stop)
    print("start stop list", start_stop_valid_trips)

    # Get all trips of destination bus stop that are within a time range given either side of what user specified
    trip_id_list = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(stop_id = dest_stop, arrival_time__range = (time_range2, time_range1)))

    print("time range", trip_id_list)
    #print(len(trip_id_list))

    # Narrow the trips to those that have service on todays date
    dest_stop_valid_trips = list(Trips.objects.values_list('trip_id', flat = True).filter(trip_id__in = trip_id_list, service_id__in = service_list))
    print("day of service too", dest_stop_valid_trips)

    # Create a multi route object from the two lists of trip IDs
    route = MultiRoute(weather, weekday, time_period, start_stop, dest_stop, start_stop_valid_trips, dest_stop_valid_trips)

    print("Multi routing")
    return "multi_routing"







class Route():
    '''
    A subclass of Route class that is composed of 2 routes to create a multi route

    Some attributes are handled differently due to these routes not sharing common stops on one trip
    '''

    def __init__(self, weather, weekday, time_period, start_stop, dest_stop):
        self.weather = weather
        self.weekday = weekday
        self.time_period = time_period
        #self.direction

        self.start_stop_id = start_stop.stop_id
        self.start_stop_id_short = start_stop.stop_id_short
        self.dest_stop_id = dest_stop.stop_id
        self.dest_stop_id_short = dest_stop.stop_id_short



# dest_trip_dict = {}
# start_trip_dict = {}
#
# for trip in dest_stop_valid_trips:
#     trips_query_set = Trips.objects.filter(trip_id = trip).values_list('route_id', 'trip_headsign', 'shape_id')
#
#     route_id = trips_query_set[0][0]
#     trip_headsign = trips_query_set[0][1]
#     shape_id = trips_query_set[0][2]
#     #print(trips_query_set)
#     #print(route_id, trip_headsign, shape_id)
#     route_short_name = Routes.objects.filter(route_id = route_id).values_list('route_short_name', flat = True)[0]
#     #print(route_short_name)
#
#     dest_trip_dict[trip] = MultiRoute(weather, weekday, time_period, start_stop, dest_stop, trip, route_id, route_short_name, trip_headsign, shape_id)






class MultiRoute(Route):
    '''
    '''

    def __init__(self, weather, weekday, time_period, start_stop, dest_stop, start_stop_valid_trips, dest_stop_valid_trips):
        Route.__init__(self, weather, weekday, time_period, start_stop, dest_stop)
        self.x = start_stop_valid_trips
        self.y = dest_stop_valid_trips

        self.display_route_details()

    def display_route_details(self):
        '''
        Simple function that prints attributes to terminal, useful for development
        '''

        print("************************************")
        print("Route from", self.start_stop_id, "to", self.dest_stop_id)
        print("Weather:", self.weather, "\nWeekday:", self.weekday, "\nTime Period:", self.time_period)
        print("Start stops valid:", self.x)
        print("Dest stops valid:", self.y)
        print("************************************")





class DirectRoute(Route):
    '''
    Class that represents a direct route between the two stops
    '''

    def __init__(self, weather, weekday, time_period, start_stop, dest_stop, trip_id, route_id, route_short_name, trip_headsign, shape_id):
        Route.__init__(self, weather, weekday, time_period, start_stop, dest_stop)
        self.route_id = route_id
        self.trip_id = trip_id
        self.route_short_name = route_short_name
        self.trip_headsign = trip_headsign
        self.shape_id = shape_id
        self.start_stop_distance = self.get_stop_distance(self.start_stop_id)
        self.dest_stop_distance = self.get_stop_distance(self.dest_stop_id)

        self.all_stops_list = self.get_all_stops()
        self.subroute_stops_list = self.get_subroute_stops()
        self.route_shape_points = self.get_all_shape_points()
        self.subroute_shape_points = self.get_subroute_shape_points()
        self.number_stops = len(self.subroute_stops_list) - 1
        self.departure_time

        self.display_route_details()


    def get_all_stops(self):
        '''
        Function that returns a list of stops as a dictionary object and assigns it
        to self.all_stops_list.
        This dictionary contains stop name, id, lat, lng, stop_sequence, due_arrival_time,
        distance travelled and distance from previous stop.
        Query based on trip_id
        Assigns deptarture time

        '''

        stops = []
        stop_ids = list(MapTripStopTimes.objects.filter(trip_id = self.trip_id).values_list('stop_id','stop_sequence', 'arrival_time', 'shape_dist_traveled'))

        self.departure_time = stop_ids[0][2]
        #print(self.departure_time)
        #print(stops)

        for stop in stop_ids:
            #print(stop)
            #print(stop[0])
            stop_dict = {}
            stops_query_set = Stops.objects.filter(stop_id = stop[0]).values_list('stop_name', 'stop_lat', 'stop_lng', 'stop_id_short')
            #print(stops_query_set)

            stop_dict["stop_id"] = stop[0]
            stop_dict["stop_id_short"] = stops_query_set[0][3]
            stop_dict["stop_name"] = stops_query_set[0][0]
            stop_dict["stop_lat"] = stops_query_set[0][1]
            stop_dict["stop_lng"] = stops_query_set[0][2]
            stop_dict["stop_sequence"] = stop[1]
            stop_dict["due_arrival_time"] = stop[2]

            predicted_diff_in_time = predict(self.weather, self.time_period, self.weekday, self.route_short_name, stop_dict["stop_sequence"], 0)

            due_time = datetime.datetime.strptime(stop_dict["due_arrival_time"], "%H:%M:%S")

            #print(due_time)
            predicted_diff_in_time = (due_time + datetime.timedelta(seconds=predicted_diff_in_time)).time()
            stop_dict["predicted_arrival_time"] = predicted_diff_in_time


            if stop[3] == None:
                previous_dist_travelled = 0
                stop_dict["shape_distance_travelled"] = 0
                stop_dict["distance_from_previous"] = 0

            else:
                stop_dict["shape_distance_travelled"] = stop[3]
                stop_dict["distance_from_previous"] = stop[3] - previous_dist_travelled

            previous_dist_travelled = stop_dict["shape_distance_travelled"]
            #print(stop_dict)
            stops.append(stop_dict)

        #print(stops)
        return stops


    def get_subroute_stops(self):
        '''
        Returns a list of tuples which contain the stop ID and stop sequence number.
        Uses the start and dest stop sequence along this trip/route to slice a subset of stops.
        '''
        stops = []

        for stop_dict in self.all_stops_list:
            #print(stop_dict)
            #print(tup[0], self.start_stop_id)
            if stop_dict["stop_id"] == self.start_stop_id:
                start_seq = stop_dict["stop_sequence"]
                #print(start_seq)

            elif stop_dict["stop_id"] == self.dest_stop_id:
                dest_seq = stop_dict["stop_sequence"]
                #print(dest_seq)

        max_stop_order = max(start_seq,dest_seq)
        min_stop_order = min(start_seq,dest_seq)

        for stop_dict in self.all_stops_list:
            stop_sequence = stop_dict["stop_sequence"]
            #print(stop_sequence)
            if stop_sequence <= max_stop_order and stop_sequence >= min_stop_order:
                stops.append(stop_dict)
        #print(stops)
        return stops


    def get_stop_distance(self, stop_id):
        '''
        Function that gets distance travelled to reach a specififed stop id.
        Used by get_subroute_shape_points function to identify start and stop
        of sub route shape
        '''

        shape_distance_travelled = MapTripStopTimes.objects.filter(trip_id = self.trip_id, stop_id = stop_id).values_list('shape_dist_traveled', flat = True)[0]
        #print(shape_distance_travelled)
        return shape_distance_travelled


    def get_all_shape_points(self):
        '''
        Function that returns all the shape points for a route
        '''

        shape_points = list(Shapes.objects.filter(shape_id = self.shape_id).values('shape_point_sequence', 'shape_point_lat', 'shape_point_lng', 'shape_dist_travelled'))
        #print(shape_points)

        return shape_points


    def get_subroute_shape_points(self):
        '''
        Function that returns all the shape points for a subroute
        '''

        shape_points = []
        for point in self.route_shape_points:
            #print(point[3])
            if point["shape_dist_travelled"] == self.start_stop_distance:
                start_seq = point["shape_point_sequence"]
            elif point["shape_dist_travelled"] == self.dest_stop_distance:
                dest_seq = point["shape_point_sequence"]

        max_seq = max(start_seq, dest_seq)
        min_seq = min(start_seq, dest_seq)

        for point in self.route_shape_points:
            shape_seq = point["shape_point_sequence"]

            if shape_seq >= min_seq and shape_seq <= max_seq:
                #print(point)
                shape_points.append(point)

        return shape_points

    def display_route_details(self):
        '''
        Simple function that prints attributes to terminal, useful for development
        '''

        print("************************************")
        print("Weather:", self.weather, "\nWeekday:", self.weekday, "\nTime Period:", self.time_period)
        print("Route from", self.start_stop_id, "to", self.dest_stop_id)
        print("Trip ID:", self.trip_id, "\nRoute ID:", self.route_id)
        print("Route Name:", self.route_short_name, "Headsign:", self.trip_headsign)
        print("Shape ID:", self.shape_id)
        print("Start stop distance:", self.start_stop_distance, "End Stop distance:", self.dest_stop_distance)
        print("ALL STOPS:\n", self.all_stops_list)
        print("SUB ROUTE STOPS:\n", self.subroute_stops_list)
        print("ALL SHAPE POINTS:\n", self.route_shape_points)
        print("SUBROUTE SHAPE POINTS:\n", self.subroute_shape_points)
        print("************************************")




































def predict(weather, time_period, weekday, route_short_name, PROGRNUMBER, direction):

    #Also take time and date as parameters
    #Somehow get direction from information

    #time_period = time_period
    time_period = 1

    #weather = weather
    rain = 0.5
    #Get weekday/weekend
    #weekday = weekday

    if direction == 1:
        direction = True
    else:
        direction = False

    dataframe = pd.DataFrame([(PROGRNUMBER, time_period, direction, rain)], columns=('PROGRNUMBER',  'Time_period', 'DIRECTION', 'rain'))
    features = ['PROGRNUMBER', 'Time_period', 'DIRECTION', 'rain']

    try:
        file = 'map/pickles/' + str(route_short_name)  + '_bus_model.sav'
        linear_model = pickle.load(open(file, 'rb'))

    except FileNotFoundError:
        file = 'map/pickles/generic_bus_model.sav'
        linear_model = pickle.load(open(file, 'rb'))

    time_diff = int((linear_model.predict(dataframe[features]))[0])

    return time_diff
