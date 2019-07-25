
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
    time_specified = (datetime.datetime.now()+ datetime.timedelta(minutes=60)).strftime('%H:%M:%S')
    #print(time_specified)
    # Convert date to week or weekend

    start_stop = "8220DB001069"
    dest_stop = "8220DB000670"

    # start_stop = 1069
    # dest_stop = 670

    # start_stop = 1052
    # dest_stop = 7245

    start_stop = 1069
    dest_stop = 93

    # start_stop = 1069
    # dest_stop = 22

    start_stop = Stops.objects.get(stop_id_short = start_stop)
    dest_stop = Stops.objects.get(stop_id_short = dest_stop)

    date_time = datetime.datetime.now()
    time = datetime.datetime.now().strftime('%H:%M:%S')
    todays_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Monday is 0
    day = datetime.datetime.today().weekday()

    time_range1 = (datetime.datetime.now() + datetime.timedelta(minutes=80)).strftime('%H:%M:%S')
    time_range2 = (datetime.datetime.now() + datetime.timedelta(minutes=60)).strftime('%H:%M:%S')
    time_range3 = (datetime.datetime.now() + datetime.timedelta(minutes=120)).strftime('%H:%M:%S')

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
    data = []

    # If no common trips between stops
    if len(common_trip_id_list) == 0:
        print("No common route found")

        valid_start_stop_trip_ids = valid_trip_id_list

        # Dest stop trip ids within a larger time frame
        dest_stop_trip_ids = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(stop_id = dest_stop, arrival_time__range = (time_range2, time_range3)))
        valid_dest_stop_trip_ids = list(Trips.objects.values_list('trip_id', flat = True).filter(trip_id__in = dest_stop_trip_ids, service_id__in = service_list))


        travel_options = MultiRoute(weather, weekday, time_specified, time_period, start_stop, dest_stop, valid_start_stop_trip_ids, valid_dest_stop_trip_ids)

    else:
        travel_options = DirectRoutes(weather, weekday, time_specified, time_period, start_stop, dest_stop, common_trip_id_list)
        print(travel_options.common_trips_dict)

        for trip in travel_options.common_trips_dict:

            # Check trip is valid
            if travel_options.common_trips_dict[trip].valid:

                route_option_dict ={}

                route_option_dict["route_id"] = travel_options.common_trips_dict[trip].route_id
                route_option_dict["trip_id"] = travel_options.common_trips_dict[trip].trip_id
                route_option_dict["route_short_name"] = travel_options.common_trips_dict[trip].route_short_name
                route_option_dict["trip_headsign"] = travel_options.common_trips_dict[trip].trip_headsign
                route_option_dict["start_stop_id"] = travel_options.common_trips_dict[trip].start_stop_id
                route_option_dict["dest_stop_id"] = travel_options.common_trips_dict[trip].dest_stop_id
                route_option_dict["start_stop_id_short"] = travel_options.common_trips_dict[trip].start_stop_id_short
                route_option_dict["dest_stop_id_short"] = travel_options.common_trips_dict[trip].dest_stop_id_short
                route_option_dict["number_stops"] = travel_options.common_trips_dict[trip].number_stops
                route_option_dict["departure_time"] = travel_options.common_trips_dict[trip].departure_time
                route_option_dict["all_stops_list"] = travel_options.common_trips_dict[trip].all_stops_list
                route_option_dict["subroute_stops_list"] = travel_options.common_trips_dict[trip].subroute_stops_list
                route_option_dict["route_shape_points"] = travel_options.common_trips_dict[trip].route_shape_points
                route_option_dict["subroute_shape_points"] = travel_options.common_trips_dict[trip].subroute_shape_points

                data.append(route_option_dict)

    # for trip in common_trip_id_list:
    #     route_dict = {}
    #
    #     #print(trip)
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
    #     # Create a direct route object that holds all the details for this route
    #     # Pass weather, time period etc in here
    #     temp_route_dict[trip] = DirectRoute(weather, weekday, time_range2, time_period, start_stop, dest_stop, trip, route_id, route_short_name, trip_headsign, shape_id)
    #
    #     #Check route is valid
    #     if temp_route_dict[trip].valid:
    #
    #         route_dict["route_id"] = temp_route_dict[trip].route_id
            # route_dict["trip_id"] = temp_route_dict[trip].trip_id
            # route_dict["route_short_name"] = temp_route_dict[trip].route_short_name
            # route_dict["trip_headsign"] = temp_route_dict[trip].trip_headsign
            # route_dict["start_stop_id"] = temp_route_dict[trip].start_stop_id
            # route_dict["dest_stop_id"] = temp_route_dict[trip].dest_stop_id
            # route_dict["start_stop_id_short"] = temp_route_dict[trip].start_stop_id_short
            # route_dict["dest_stop_id_short"] = temp_route_dict[trip].dest_stop_id_short
            # route_dict["number_stops"] = temp_route_dict[trip].number_stops
            # route_dict["departure_time"] = temp_route_dict[trip].departure_time
            # route_dict["all_stops_list"] = temp_route_dict[trip].all_stops_list
            # route_dict["subroute_stops_list"] = temp_route_dict[trip].subroute_stops_list
            # route_dict["route_shape_points"] = temp_route_dict[trip].route_shape_points
            # route_dict["subroute_shape_points"] = temp_route_dict[trip].subroute_shape_points
    #
    #         data.append(route_dict)

    return JsonResponse({'routes_data': data})
    #return HttpResponse("yep")



# def multi_routing(weather, weekday, time_period, start_stop_valid_trip_id_list, start_stop, dest_stop, time_range1, time_range2, service_list):
#     #start_stop = start_stop
#     #dest_stop = dest_stop
#
#     start_stop_valid_trips = start_stop_valid_trip_id_list
#     print(start_stop, dest_stop)
#     print("start stop list", start_stop_valid_trips)
#
#     # Get all trips of destination bus stop that are within a time range given either side of what user specified
#     # Give more time to this stop??
#     trip_id_list = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(stop_id = dest_stop, arrival_time__range = (time_range2, time_range1)))
#
#     print("time range", trip_id_list)
#     #print(len(trip_id_list))
#
#     # Narrow the trips to those that have service on todays date
#     dest_stop_valid_trips = list(Trips.objects.values_list('trip_id', flat = True).filter(trip_id__in = trip_id_list, service_id__in = service_list))
#     print("day of service too", dest_stop_valid_trips)
#
#     # Create a multi route object from the two lists of trip IDs
#     route = MultiRoute(weather, weekday, time_period, start_stop, dest_stop, start_stop_valid_trips, dest_stop_valid_trips)
#
#     print("Multi routing")
#     return "multi_routing"

# def multi_routing(start_trip_ids, dest_trip_ids, weather, weekday, time, time_period, start_stop, dest_stop):
#     print("Multi-routing\n")
#     print("Starting stop trips:",start_trip_ids,"\n")
#     print("Dest stop trip ids:",dest_trip_ids,"\n")
#     print()
#
#
#     #dest_stop = "8220DB000670"
#     #dest_stop = Stops.objects.get(stop_id_short = 670)
#     #y = Trip('5850.3.60-14-d12-1.127.I', weather, weekday, time, time_period, start_stop, dest_stop)
#     x = MultiRoute(weather, weekday, time, time_period, start_stop, dest_stop, start_trip_ids, dest_trip_ids)
#
#     return HttpResponse("Multi Routing")





class Route():
    '''

    '''

    def __init__(self, weather, weekday, time, time_period, start_stop, dest_stop):
        self.weather = weather
        self.weekday = weekday
        self.time_period = time_period
        #self.direction

        self.time = time
        time = time.split(":")
        hour = int(time[0])
        min = int(time[1])
        sec = int(time[2])
        self.time_specified = datetime.time(hour, min, sec)

        self.start_stop = start_stop
        self.dest_stop = dest_stop
        self.start_stop_id = start_stop.stop_id
        self.start_stop_id_short = start_stop.stop_id_short
        self.dest_stop_id = dest_stop.stop_id
        self.dest_stop_id_short = dest_stop.stop_id_short


class DirectRoutes(Route):
    '''
    '''

    def __init__(self, weather, weekday, time, time_period, start_stop, dest_stop, common_trip_ids):
        Route.__init__(self, weather, weekday, time, time_period, start_stop, dest_stop)
        self.common_trip_ids = common_trip_ids
        self.common_trips_dict = self.create_trips(self.common_trip_ids)

    def create_trips(self, common_trip_ids):
        trip_dict = {}

        for trip in common_trip_ids:
            trip_dict[trip] = Trip(trip, self.weather, self.weekday, self.time, self.time_period, self.start_stop, self.dest_stop)

        return trip_dict


class MultiRoute(Route):
    '''
    '''

    def __init__(self, weather, weekday, time, time_period, start_stop, dest_stop, start_trip_ids, dest_trip_ids):
        Route.__init__(self, weather, weekday, time, time_period, start_stop, dest_stop)
        self.start_trip_ids = start_trip_ids
        self.dest_trip_ids = dest_trip_ids
        self.start_trips_dict = self.create_start_trips(self.start_trip_ids)
        self.dest_trips_dict = self.create_dest_trips(self.dest_trip_ids)

        self.display_route_details()
        self.check_for_common_stops()


    def create_trips_and_check(self):

        return True

    def create_start_trips(self, trip_id_list):
        trip_dict = {}

        for trip in trip_id_list:
            trip_dict[trip] = Trip(trip, self.weather, self.weekday, self.time, self.time_period, self.start_stop, None)

            # If arrival time is before time specified then delete
            if trip_dict[trip].valid == False:
                #print("Deleting trip", trip, "from dict because", trip_dict[trip].predicted_start_arrival_time )
                del trip_dict[trip]

        return trip_dict

    def create_dest_trips(self, trip_id_list):
        trip_dict = {}

        for trip in trip_id_list:
            trip_dict[trip] = Trip(trip, self.weather, self.weekday, self.time, self.time_period, None, self.dest_stop)

        return trip_dict

    def check_for_common_stops(self):

        options_count = 0
        for trip_key in self.dest_trips_dict:
            #print("Dest trip", count)
            #print(self.dest_trips_dict[trip_key].subroute_stops_list)
            for stop in self.dest_trips_dict[trip_key].subroute_stops_list:

                used_route = False

                for trip_key2 in self.start_trips_dict:

                    if used_route == True:
                        break
                    #print("Start trip", count2)
                    #print(self.start_trips_dict[trip_key2].predicted_start_arrival_time)
                    #print("Start stop trip",self.start_trips_dict[trip_key2].subroute_stops_list)


                    for stop2 in self.start_trips_dict[trip_key2].subroute_stops_list:

                        if stop["stop_id"] == stop2["stop_id"]:
                            #print("MATCH!Route:",self.dest_trips_dict[trip_key].route_short_name,"Stop", stop["stop_id_short"], \
                            #        "VERSUS Route:", self.start_trips_dict[trip_key2].route_short_name,"Stop", stop2["stop_id_short"])

                            first_leg_arrival = stop["predicted_arrival_time"]
                            first_leg_seconds = (first_leg_arrival.hour * 60 + first_leg_arrival.minute) * 60 + first_leg_arrival.second

                            second_leg_dept = stop2["predicted_arrival_time"]
                            second_leg_seconds = (second_leg_dept.hour * 60 + second_leg_dept.minute) * 60 + second_leg_dept.second

                            wait_time_seconds = second_leg_seconds - first_leg_seconds

                            # Add in max waiting time
                            max_wait_time_seconds = 30 * 60

                            if first_leg_seconds < second_leg_seconds and wait_time_seconds < max_wait_time_seconds:

                                common_stop = stop["stop_id"]
                                #print(second_leg_dept - first_leg_arrival)
                                #print("VALID!!!******Arrive", first_leg_arrival, "deptarture", second_leg_dept)
                                print("VALID OPTION:", options_count + 1, " \nRoute ID -",self.start_trips_dict[trip_key2].route_short_name,"from", self.start_stop_id,\
                                        "to", common_stop,"arrives at", first_leg_arrival,"wait",wait_time_seconds/60,"mins then get Route",\
                                        self.dest_trips_dict[trip_key].route_short_name,"to",self.dest_stop_id)
                                options_count += 1
                                used_route = True

                                if options_count >= 500:
                                    return
                                else:
                                    break
        return


    def display_route_details(self):
        '''
        Simple function that prints attributes to terminal, useful for development
        '''

        print("************************************")
        print("Weather:", self.weather, "\nWeekday:", self.weekday, "\nTime Period:", self.time_period)
        print("Route from", self.time_specified)
        print("Route from", self.start_stop_id_short, "to", self.dest_stop_id_short)
        print("Route from", self.start_stop_id, "to", self.dest_stop_id)
        print("Start stop trips:", self.start_trip_ids)
        print("Dest stop trips:", self.dest_trip_ids)
        print("Start trip dict:", self.start_trips_dict)
        print("Dest trip dict:", self.dest_trips_dict)
        print("************************************")

class Trip():
    '''
    '''

    def __init__(self, trip_id, weather, weekday, time, time_period, start_stop = None, dest_stop = None):

        self.trip_id = trip_id
        self.weather = weather
        self.weekday = weekday
        self.time_period = time_period
        #self.direction

        time = time.split(":")
        hour = int(time[0])
        min = int(time[1])
        sec = int(time[2])
        self.time_specified = datetime.time(hour, min, sec)

        if start_stop:
            #print("Start stop")
            self.start_stop = start_stop
            self.start_stop_id = start_stop.stop_id
            self.start_stop_id_short = start_stop.stop_id_short

        if dest_stop:
            #print("Dest stop")
            self.dest_stop = start_stop
            self.dest_stop_id = dest_stop.stop_id
            self.dest_stop_id_short = dest_stop.stop_id_short


        trips_query_set = Trips.objects.filter(trip_id = self.trip_id).values_list('route_id', 'trip_headsign', 'shape_id')
        #print(trips_query_set)

        self.route_id = trips_query_set[0][0]
        self.trip_headsign = trips_query_set[0][1]
        self.shape_id = trips_query_set[0][2]
        self.route_short_name = Routes.objects.filter(route_id = self.route_id).values_list('route_short_name', flat = True)[0]

        self.all_stops_list = self.get_all_stops()
        self.subroute_stops_list = self.get_subroute_stops()
        self.number_stops = len(self.subroute_stops_list) - 1

        self.route_shape_points = self.get_all_shape_points()
        self.subroute_shape_points = self.get_subroute_shape_points()


        #self.display_route_details()


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

        stop_sequence_list = list(MapTripStopTimes.objects.filter(trip_id = self.trip_id).values_list('stop_sequence', flat = True))

        self.departure_time = stop_ids[0][2]
        #print(self.departure_time)
        #print(stops)

        # Use self. in time
        weather_temp = 20
        weather_rain = 0
        time_period = 1
        weekday = 1
        route_short_name = self.route_short_name
        stop_sequence_list = stop_sequence_list
        direction = 1

        stop_seq_time_diff_dict = predict(weather_temp, weather_rain, time_period, weekday, route_short_name, stop_sequence_list, direction)



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

            #predicted_diff_in_time = predict(self.weather, self.time_period, self.weekday, self.route_short_name, stop_dict["stop_sequence"], 0)
            stop_sequence = stop[1]
            predicted_diff_in_time = stop_seq_time_diff_dict[stop_sequence]
            #print(predicted_diff_in_time)

            due_time = datetime.datetime.strptime(stop_dict["due_arrival_time"], "%H:%M:%S")

            #print(due_time)
            predicted_arrival_time = (due_time + datetime.timedelta(seconds=predicted_diff_in_time)).time()
            #print(predicted_arrival_time)
            stop_dict["predicted_arrival_time"] = predicted_arrival_time


            if hasattr(self, 'start_stop') and stop[0] == self.start_stop_id:
                self.predicted_start_arrival_time = predicted_arrival_time
                #print(self.predicted_start_arrival_time)

                # Check if valid, maybe terminate if not
                self.check_valid()
                #print(start_seq)


            if stop[3] == None:
                previous_dist_travelled = 0
                stop_dict["shape_distance_travelled"] = 0
                stop_dict["distance_from_previous"] = 0

            else:
                stop_dict["shape_distance_travelled"] = stop[3]
                stop_dict["distance_from_previous"] = stop[3] - previous_dist_travelled

            if hasattr(self, 'start_stop') and stop[0] == self.start_stop_id:
                self.start_stop_sequence = stop[1]

                if stop[3] == None:
                    self.start_stop_distance = 0
                else:
                    self.start_stop_distance = stop[3]


            if hasattr(self, 'dest_stop') and stop[0] == self.dest_stop_id:

                self.dest_stop_sequence = stop[1]

                if stop[3] == None:
                    self.dest_stop_distance = 0
                else:
                    self.dest_stop_distance = stop[3]

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

        # Check which type of subroute is needed
        # Has start and dest stop IDs e.g Direct Route
        if all(hasattr(self, attr) for attr in ["start_stop", "dest_stop"]):
            #print("Has both")

            end_stop_order = max(self.start_stop_sequence,self.dest_stop_sequence)
            start_stop_order = min(self.start_stop_sequence,self.dest_stop_sequence)

            for stop_dict in self.all_stops_list:
                stop_sequence = stop_dict["stop_sequence"]
                #print(stop_sequence)
                if stop_sequence <= end_stop_order and stop_sequence >= start_stop_order:
                    stops.append(stop_dict)

        # Has just start stop ID specfied, start to end subroute
        elif hasattr(self, 'start_stop'):
            #print("Has start")

            for stop_dict in self.all_stops_list:
                stop_sequence = stop_dict["stop_sequence"]
                #print(stop_sequence)
                if stop_sequence >= self.start_stop_sequence:
                    stops.append(stop_dict)

        # Has just dest ID specified, all to dest subroute
        elif hasattr(self, 'dest_stop'):
            #print("Has dest")

            for stop_dict in self.all_stops_list:
                stop_sequence = stop_dict["stop_sequence"]
                #print(stop_sequence)
                if stop_sequence <= self.dest_stop_sequence:
                    stops.append(stop_dict)

        #print(stops)
        return stops



    def check_valid(self):
        '''
        '''

        if self.predicted_start_arrival_time < self.time_specified:

            #print("yes, delete me")
            self.valid = False

        else:
            self.valid = True


    def get_all_shape_points(self):
        '''
        Function that returns all the shape points for a route
        '''

        shape_points = list(Shapes.objects.filter(shape_id = self.shape_id).values('shape_point_sequence', 'shape_point_lat', 'shape_point_lng', 'shape_dist_travelled'))
        #print(shape_points)

        return shape_points




    def get_stop_distance(self, stop_id):
        '''
        OBSOLETE
        Function that gets distance travelled to reach a specififed stop id.
        Used by get_subroute_shape_points function to identify start and stop
        of sub route shape
        '''

        shape_distance_travelled = MapTripStopTimes.objects.filter(trip_id = self.trip_id, stop_id = stop_id).values_list('shape_dist_traveled', flat = True)[0]
        #print(shape_distance_travelled)
        return shape_distance_travelled


    def get_subroute_shape_points(self):
        '''
        Function that returns all the shape points for a subroute
        '''

        shape_points = []


        if all(hasattr(self, attr) for attr in ["start_stop", "dest_stop"]):
            #print("Has both for sub shape points")

            for point in self.route_shape_points:

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


        elif hasattr(self, 'start_stop'):
            for point in self.route_shape_points:

                if point["shape_dist_travelled"] == self.start_stop_distance:
                    start_seq = point["shape_point_sequence"]
                    break

            for point in self.route_shape_points:
                shape_seq = point["shape_point_sequence"]

                if shape_seq >= start_seq:
                    #print(point)
                    shape_points.append(point)


        elif hasattr(self, 'dest_stop'):
            for point in self.route_shape_points:

                if point["shape_dist_travelled"] == self.dest_stop_distance:
                    end_seq = point["shape_point_sequence"]
                    break

            for point in self.route_shape_points:
                shape_seq = point["shape_point_sequence"]

                if shape_seq <= end_seq:
                    #print(point)
                    shape_points.append(point)

        return shape_points



    def display_route_details(self):
        '''
        Simple function that prints attributes to terminal, useful for development
        '''

        print("************************************")
        print("TRIP")
        print("Weather:", self.weather, "\nWeekday:", self.weekday, "\nTime Period:", self.time_period)
        print("Route from", self.time_specified)
        if hasattr(self, 'start_stop'):
            print("Start stop", self.start_stop_id_short, self.start_stop_id)
        if hasattr(self, 'dest_stop'):
            print("Dest stop", self.dest_stop_id_short, self.dest_stop_id)
        print("Trip ID:", self.trip_id, "\nRoute ID:", self.route_id)
        print("Route Name:", self.route_short_name, "Headsign:", self.trip_headsign)
        print("Shape ID:", self.shape_id)
        print("All stops for trip:", self.all_stops_list)
        print("Sub Route stops", self.subroute_stops_list)
        print("All Route Shape Points", self.route_shape_points)
        print("Sub route shape points", self.subroute_shape_points)
        print("Length of trip:", self.number_stops)
        if hasattr(self, 'start_stop'):
            print(self.start_stop_distance)
        if hasattr(self, 'dest_stop'):
            print(self.dest_stop_distance)
        print("************************************")



# class DirectRoute(Route):
#     '''
#     Class that represents a direct route between the two stops
#     '''
#
#     def __init__(self, weather, weekday, time, time_period, start_stop, dest_stop, trip_id, route_id, route_short_name, trip_headsign, shape_id):
#         Route.__init__(self, weather, weekday, time, time_period, start_stop, dest_stop)
#         self.route_id = route_id
#         self.trip_id = trip_id
#         self.route_short_name = route_short_name
#         self.trip_headsign = trip_headsign
#         self.shape_id = shape_id
#         self.start_stop_distance = self.get_stop_distance(self.start_stop_id)
#         self.dest_stop_distance = self.get_stop_distance(self.dest_stop_id)
#
#         self.all_stops_list = self.get_all_stops()
#         self.subroute_stops_list = self.get_subroute_stops()
#         self.route_shape_points = self.get_all_shape_points()
#         self.subroute_shape_points = self.get_subroute_shape_points()
#         self.number_stops = len(self.subroute_stops_list) - 1
#         self.departure_time
#
#         #self.display_route_details()
#
#     def check_valid(self):
#         '''
#         '''
#
#         if self.predicted_start_arrival_time < self.time_specified:
#
#             #print("yes, delete me")
#             self.valid = False
#
#         else:
#             self.valid = True
#
#
#     def get_all_stops(self):
#         '''
#         Function that returns a list of stops as a dictionary object and assigns it
#         to self.all_stops_list.
#         This dictionary contains stop name, id, lat, lng, stop_sequence, due_arrival_time,
#         distance travelled and distance from previous stop.
#         Query based on trip_id
#         Assigns deptarture time
#
#         '''
#         stops = []
#
#         stop_ids = list(MapTripStopTimes.objects.filter(trip_id = self.trip_id).values_list('stop_id','stop_sequence', 'arrival_time', 'shape_dist_traveled'))
#
#         stop_sequence_list = list(MapTripStopTimes.objects.filter(trip_id = self.trip_id).values_list('stop_sequence', flat = True))
#
#         self.departure_time = stop_ids[0][2]
#         #print(self.departure_time)
#         #print(stops)
#
#         # Use self. in time
#         weather_temp = 20
#         weather_rain = 0
#         time_period = 1
#         weekday = 1
#         route_short_name = self.route_short_name
#         stop_sequence_list = stop_sequence_list
#         direction = 1
#
#         stop_seq_time_diff_dict = predict(weather_temp, weather_rain, time_period, weekday, route_short_name, stop_sequence_list, direction)
#
#
#
#         for stop in stop_ids:
#             #print(stop)
#             #print(stop[0])
#             stop_dict = {}
#             stops_query_set = Stops.objects.filter(stop_id = stop[0]).values_list('stop_name', 'stop_lat', 'stop_lng', 'stop_id_short')
#             #print(stops_query_set)
#
#             stop_dict["stop_id"] = stop[0]
#             stop_dict["stop_id_short"] = stops_query_set[0][3]
#             stop_dict["stop_name"] = stops_query_set[0][0]
#             stop_dict["stop_lat"] = stops_query_set[0][1]
#             stop_dict["stop_lng"] = stops_query_set[0][2]
#             stop_dict["stop_sequence"] = stop[1]
#             stop_dict["due_arrival_time"] = stop[2]
#
#             #predicted_diff_in_time = predict(self.weather, self.time_period, self.weekday, self.route_short_name, stop_dict["stop_sequence"], 0)
#             stop_sequence = stop[1]
#             predicted_diff_in_time = stop_seq_time_diff_dict[stop_sequence]
#             #print(predicted_diff_in_time)
#
#             due_time = datetime.datetime.strptime(stop_dict["due_arrival_time"], "%H:%M:%S")
#
#             #print(due_time)
#             predicted_arrival_time = (due_time + datetime.timedelta(seconds=predicted_diff_in_time)).time()
#             #print(predicted_arrival_time)
#             stop_dict["predicted_arrival_time"] = predicted_arrival_time
#
#
#             if stop[3] == None:
#                 previous_dist_travelled = 0
#                 stop_dict["shape_distance_travelled"] = 0
#                 stop_dict["distance_from_previous"] = 0
#
#             else:
#                 stop_dict["shape_distance_travelled"] = stop[3]
#                 stop_dict["distance_from_previous"] = stop[3] - previous_dist_travelled
#
#             previous_dist_travelled = stop_dict["shape_distance_travelled"]
#             #print(stop_dict)
#             stops.append(stop_dict)
#
#         #print(stops)
#         return stops
#
#
#     def get_subroute_stops(self):
#         '''
#         Returns a list of tuples which contain the stop ID and stop sequence number.
#         Uses the start and dest stop sequence along this trip/route to slice a subset of stops.
#         '''
#         stops = []
#
#         # # Check for multi routing sub route
#         # if self.start_stop_id == self.dest_stop_id:
#         #     for stop_dict in self.all_stops_list:
#         #         if stop_dict["stop_id"] == self.start_stop_id:
#         #             start_seq = stop_dict["stop_sequence"]
#         #
#         #     for stop_dict in self.all_stops_list:
#         #         stop_sequence = stop_dict["stop_sequence"]
#         #         if stop_sequence >= start_seq:
#         #             stops.append(stop_dict)
#         #
#         # # Normal case
#         # else:
#         for stop_dict in self.all_stops_list:
#             #print(stop_dict)
#             #print(tup[0], self.start_stop_id)
#             if stop_dict["stop_id"] == self.start_stop_id:
#                 start_seq = stop_dict["stop_sequence"]
#
#                 self.predicted_start_arrival_time = stop_dict["predicted_arrival_time"]
#                 #print(self.predicted_start_arrival_time)
#
#                 # Check if valid
#                 self.check_valid()
#                 #print(start_seq)
#
#             elif stop_dict["stop_id"] == self.dest_stop_id:
#                 dest_seq = stop_dict["stop_sequence"]
#                 #print(dest_seq)
#
#         max_stop_order = max(start_seq,dest_seq)
#         min_stop_order = min(start_seq,dest_seq)
#
#         for stop_dict in self.all_stops_list:
#             stop_sequence = stop_dict["stop_sequence"]
#             #print(stop_sequence)
#             if stop_sequence <= max_stop_order and stop_sequence >= min_stop_order:
#                 stops.append(stop_dict)
#         #print(stops)
#         return stops
#
#
#     def get_stop_distance(self, stop_id):
#         '''
#         Function that gets distance travelled to reach a specififed stop id.
#         Used by get_subroute_shape_points function to identify start and stop
#         of sub route shape
#         '''
#
#         shape_distance_travelled = MapTripStopTimes.objects.filter(trip_id = self.trip_id, stop_id = stop_id).values_list('shape_dist_traveled', flat = True)[0]
#         #print(shape_distance_travelled)
#         return shape_distance_travelled
#
#
#     def get_all_shape_points(self):
#         '''
#         Function that returns all the shape points for a route
#         '''
#
#         shape_points = list(Shapes.objects.filter(shape_id = self.shape_id).values('shape_point_sequence', 'shape_point_lat', 'shape_point_lng', 'shape_dist_travelled'))
#         #print(shape_points)
#
#         return shape_points
#
#
#     def get_subroute_shape_points(self):
#         '''
#         Function that returns all the shape points for a subroute
#         '''
#
#         shape_points = []
#
#         # # Check for multi routing sub route
#         # if self.start_stop_id == self.dest_stop_id:
#         #     for point in self.route_shape_points:
#         #         if point["shape_dist_travelled"] == self.start_stop_distance:
#         #             start_seq = point["shape_point_sequence"]
#         #
#         #     for point in self.route_shape_points:
#         #         shape_seq = point["shape_point_sequence"]
#         #
#         #         if shape_seq >= start_seq:
#         #             shape_points.append(point)
#         #
#         #
#         #
#         # # Normal case
#         # else:
#         for point in self.route_shape_points:
#             #print(point[3])
#             if point["shape_dist_travelled"] == self.start_stop_distance:
#                 start_seq = point["shape_point_sequence"]
#             elif point["shape_dist_travelled"] == self.dest_stop_distance:
#                 dest_seq = point["shape_point_sequence"]
#
#         max_seq = max(start_seq, dest_seq)
#         min_seq = min(start_seq, dest_seq)
#
#         for point in self.route_shape_points:
#             shape_seq = point["shape_point_sequence"]
#
#             if shape_seq >= min_seq and shape_seq <= max_seq:
#                 #print(point)
#                 shape_points.append(point)
#
#         return shape_points
#
#     def display_route_details(self):
#         '''
#         Simple function that prints attributes to terminal, useful for development
#         '''
#
#         print("************************************")
#         print("Weather:", self.weather, "\nWeekday:", self.weekday, "\nTime Period:", self.time_period)
#         print("Route from", self.start_stop_id, "to", self.dest_stop_id)
#         print("Trip ID:", self.trip_id, "\nRoute ID:", self.route_id)
#         print("Route Name:", self.route_short_name, "Headsign:", self.trip_headsign)
#         print("Shape ID:", self.shape_id)
#         print("Start stop distance:", self.start_stop_distance, "End Stop distance:", self.dest_stop_distance)
#         print("ALL STOPS:\n", self.all_stops_list)
#         print("SUB ROUTE STOPS:\n", self.subroute_stops_list)
#         print("ALL SHAPE POINTS:\n", self.route_shape_points)
#         print("SUBROUTE SHAPE POINTS:\n", self.subroute_shape_points)
#         print("************************************")




















# class MultiRoute(Route):
#     '''
#     Multi Route is a combination of direct routes
#     '''
#
#     def __init__(self, weather, weekday, time_period, start_stop, dest_stop, start_stop_valid_trips, dest_stop_valid_trips):
#         Route.__init__(self, weather, weekday, time_period, start_stop, dest_stop)
#         self.start_stop_valid_trips = start_stop_valid_trips
#         self.dest_stop_valid_trips = dest_stop_valid_trips
#         self.dest_trips = self.generate_trips_dict(dest_stop_valid_trips, self.dest_stop)
#         self.start_trips = self.generate_trips_dict(start_stop_valid_trips, self.start_stop)
#
#         self.display_route_details()
#
#         self.check_common_stop()
#
#     def generate_trips_dict(self, trip_id_list, start_stop):
#
#         trip_dict = {}
#         for trip in trip_id_list:
#
#             trips_query_set = Trips.objects.filter(trip_id = trip).values_list('route_id', 'trip_headsign', 'shape_id')
#             route_id = trips_query_set[0][0]
#             trip_headsign = trips_query_set[0][1]
#             shape_id = trips_query_set[0][2]
#             #print(trips_query_set)
#             #print(route_id, trip_headsign, shape_id)
#             route_short_name = Routes.objects.filter(route_id = route_id).values_list('route_short_name', flat = True)[0]
#
#             # Intentionally put start_stop in twice
#             trip_dict[trip] = DirectRoute(self.weather, self.weekday, self.time_period, start_stop, start_stop, trip, route_id, route_short_name, trip_headsign, shape_id)
#
#         return trip_dict
#
#     def check_common_stop(self):
#
#         for trip in self.dest_trips:
#             print("Checking", trip, "for common stop")
#
#             for stop in self.dest_trips[trip].subroute_stops_list:
#                 check_stop = stop["stop_id"]
#                 print("Checking stop", check_stop)
#
#                 for trip2 in self.start_trips:
#                     print("Checking against", trip2)
#
#                     for stop in self.start_trips[trip2].subroute_stops_list:
#                         other_stop = stop["stop_id"]
#                         print("Checking against stop", other_stop)
#
#                         if check_stop == other_stop:
#                             print("MATCH", check_stop, "=", other_stop)
#                             return
#         print("NO MATCH")
#         return
#
#
#
#     # def get_all_stops(self, trip_id):
#     #     '''
#     #     Function that returns a list of stops as a dictionary object and assigns it
#     #     to self.all_stops_list.
#     #     This dictionary contains stop name, id, lat, lng, stop_sequence, due_arrival_time,
#     #     distance travelled and distance from previous stop.
#     #     Query based on trip_id
#     #     Assigns deptarture time
#     #
#     #     '''
#     #
#     #     stops = []
#     #     stop_ids = list(MapTripStopTimes.objects.filter(trip_id = trip_id).values_list('stop_id','stop_sequence', 'arrival_time', 'shape_dist_traveled'))
#     #
#     #     self.departure_time = stop_ids[0][2]
#     #     #print(self.departure_time)
#     #     #print(stops)
#     #
#     #     for stop in stop_ids:
#     #         #print(stop)
#     #         #print(stop[0])
#     #         stop_dict = {}
#     #         stops_query_set = Stops.objects.filter(stop_id = stop[0]).values_list('stop_name', 'stop_lat', 'stop_lng', 'stop_id_short')
#     #         #print(stops_query_set)
#     #
#     #         stop_dict["stop_id"] = stop[0]
#     #         stop_dict["stop_id_short"] = stops_query_set[0][3]
#     #         stop_dict["stop_name"] = stops_query_set[0][0]
#     #         stop_dict["stop_lat"] = stops_query_set[0][1]
#     #         stop_dict["stop_lng"] = stops_query_set[0][2]
#     #         stop_dict["stop_sequence"] = stop[1]
#     #         stop_dict["due_arrival_time"] = stop[2]
#     #
#     #         predicted_diff_in_time = predict(self.weather, self.time_period, self.weekday, self.route_short_name, stop_dict["stop_sequence"], 0)
#     #
#     #         due_time = datetime.datetime.strptime(stop_dict["due_arrival_time"], "%H:%M:%S")
#     #
#     #         #print(due_time)
#     #         predicted_diff_in_time = (due_time + datetime.timedelta(seconds=predicted_diff_in_time)).time()
#     #         stop_dict["predicted_arrival_time"] = predicted_diff_in_time
#     #
#     #
#     #         if stop[3] == None:
#     #             previous_dist_travelled = 0
#     #             stop_dict["shape_distance_travelled"] = 0
#     #             stop_dict["distance_from_previous"] = 0
#     #
#     #         else:
#     #             stop_dict["shape_distance_travelled"] = stop[3]
#     #             stop_dict["distance_from_previous"] = stop[3] - previous_dist_travelled
#     #
#     #         previous_dist_travelled = stop_dict["shape_distance_travelled"]
#     #         #print(stop_dict)
#     #         stops.append(stop_dict)
#     #
#     #     #print(stops)
#     #     return stops
#
#     def display_route_details(self):
#         '''
#         Simple function that prints attributes to terminal, useful for development
#         '''
#
#         print("*******************MULTI*****************")
#         print("Route from", self.start_stop_id, "to", self.dest_stop_id)
#         print("Weather:", self.weather, "\nWeekday:", self.weekday, "\nTime Period:", self.time_period)
#         print("Start stops trips valid:", self.start_stop_valid_trips)
#         print("Dest stops trips valid:", self.dest_stop_valid_trips)
#         print("Dest trips dict:", self.dest_trips)
#         print("Start trips dict:", self.start_trips)
#         for each in self.start_trips:
#             print(self.start_trips[each].subroute_stops_list)
#         for each in self.dest_trips:
#             print(self.dest_trips[each].subroute_stops_list)
#         print("************************************")






def predict(weather_temp, weather_rain, time_period, weekday, route_short_name, stop_sequence_list, direction = 1):
    weather_temp = 20
    weather_rain = 0.4
    time_period = 1
    weekday = 1
    direction = 1
    route_short_name = route_short_name
    stop_stop_sequence_list = stop_sequence_list
    sequence_time_diff_dict = {}

    try:
        file = 'map/pickles/' + str(route_short_name)  + '_bus_model.sav'
        linear_model = pickle.load(open(file, 'rb'))

    except FileNotFoundError:
        file = 'map/pickles/generic_bus_model.sav'
        linear_model = pickle.load(open(file, 'rb'))

    dataframe = pd.DataFrame(columns=('PROGRNUMBER',  'Time_period', 'DIRECTION', 'rain'))
    features = ['PROGRNUMBER', 'Time_period', 'DIRECTION', 'rain']

    for i in range(len(stop_stop_sequence_list)):
        dataframe.loc[i] = [stop_stop_sequence_list[i], time_period, direction, weather_rain]

    time_dif_list = linear_model.predict(dataframe[features])

    for i in range(len(time_dif_list)):
        sequence_time_diff_dict[stop_stop_sequence_list[i]] = time_dif_list[i]

    return sequence_time_diff_dict


# def predict(weather, time_period, weekday, route_short_name, PROGRNUMBER, direction):
# #def predict(request):
#     #Also take time and date as parameters
#     #Somehow get direction from information
#
#     #time_period = time_period
#     time_period = 1
#
#     #weather = weather
#     rain = 0.5
#     #Get weekday/weekend
#     #weekday = weekday
#
#     direction = 1
#
#     # if direction == 1:
#     #     direction = True
#     # else:
#     #     direction = False
#
#     dataframe = pd.DataFrame([(PROGRNUMBER, time_period, direction, rain)], columns=('PROGRNUMBER',  'Time_period', 'DIRECTION', 'rain'))
#     features = ['PROGRNUMBER', 'Time_period', 'DIRECTION', 'rain']
#
#     route_short_name = 14
#
#     try:
#         file = 'map/pickles/' + str(route_short_name)  + '_bus_model.sav'
#         linear_model = pickle.load(open(file, 'rb'))
#
#     except FileNotFoundError:
#         file = 'map/pickles/generic_bus_model.sav'
#         linear_model = pickle.load(open(file, 'rb'))
#
#
#
#
#
#     #dataframe = pd.DataFrame(columns=('PROGRNUMBER',  'Time_period', 'DIRECTION', 'rain'))
#
#     # for i in range(10):
#     #     dataframe.loc[i] = [i, time_period, direction, rain]
#     #
#     # result = linear_model.predict(dataframe[features])
#     # print(result)
#     time_diff = int((linear_model.predict(dataframe[features]))[0])
#
#     return time_diff
