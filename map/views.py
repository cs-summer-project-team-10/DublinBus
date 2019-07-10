
from django.shortcuts import render, get_object_or_404
#from .models import BusStop,RouteStops,Routes,LeaveTime,Trip,Vehicle,TrackingRawData,Justification
from .models import BusStop,RouteStops, Route
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, render, redirect
import json


# Create your views here.
def home_page(request):
    ''' Simple view that renders the index html template with all the bus stop information
        using Jinja2
    '''
    bus_stops = BusStop.objects.all()
    bus_stop_list = []
    for bus_stop in bus_stops:
        bus_stop_list.append((bus_stop.stop_id, bus_stop.stop_name, bus_stop.lat, bus_stop.lng))
    return render(request, 'map/index.html', {'JSONdata': json.dumps(bus_stop_list)})


def return_id(num):
    route_stops = RouteStops.objects.filter(stopID=num)
    route_stops_list = []
    for route_stop in route_stops:
        route_stops_list.append(route_stop.routeID.routeID)
    return route_stops_list


def return_routes(request):
    ''' Django API that will return the bus stop data as JSON data
    '''
    start_stop = request.GET['startstop']
    dest_stop = request.GET['endstop']
    list1 = return_id(start_stop)
    list2 = return_id(dest_stop)
    common = [val for val in list1 if val in list2]
    route_stops_order = []
    route_all_stops = []

    print("common: " + str(common))

    if len(common):
        for com_route in common:
            Rname=RouteStops.objects.get(route_id=com_route).line_id
            Rstops=RouteStops.objects.filter(route_id=com_route)
            for Rstop in Rstops:
                dict2 = {}
                dict2['stopid'] = Rstop.stopID.stat_number
                dict2['shortname']=BusStop.objects.get(stop_id=Rstop.stop_id.stop_id).stop_name
                dict2['latitude']=BusStop.objects.get(stop_id=Rstop.stop_id.stop_id).lat
                dict2['longitude']=BusStop.objects.get(stop_id=Rstop.stop_id.stop_id).lng
                dict2['stop_order']=Rstop.stop_order
                route_all_stops.append(dict2)
            dict={}
            dict['route_id']=com_route
            dict['line_id'] = Rname
            dict['stops'] =route_all_stops
            route_stops_order.append(dict)

        return JsonResponse({'commondata': route_stops_order})
    else:
        return JsonResponse({'commondata': route_stops_order})
        # return JsonResponse({'commondata': common})

    # return JsonResponse({'JSONdata': route_stops_list2})


class TempRoute():
    def __init__(self, line_id, route_id, start_stop, dest_stop):
        self.line_id = line_id
        self.route_id = route_id
        self.start_stop = start_stop
        self.dest_stop = dest_stop
        #self.all_stops = stop_list
        #self.number_stops = number_stops
        self.stops_serviced = self.get_stop_list()
        self.subroute = self.get_subroute()
        self.number_stops = self.get_number_stops_subroute()
        self.subroute_stop_array = self.generate_stops_array(self.subroute)
        self.stops_serviced_array = self.generate_stops_array(self.stops_serviced)

    def get_stop_list(self):
        stops_serviced = list(RouteStops.objects.values_list('stop_id', 'stop_order').filter(route_id = self.route_id))
        return stops_serviced

    def print_route(self):
        print("ROUTE on", self.route_id, self.stops_serviced)

    def print_subroute(self):
        print("SUBROUTE on ",self.route_id, self.subroute)

    def print_number_stops(self):
        print("Number stops ", self.number_stops)

    def print_lineID(self):
        print("Line ID is ", self.line_id)

    def get_subroute(self):
        subroute = []
        for tuple in self.stops_serviced:
            #print(type(tuple))
            #print(self.start_stop.stop_id)
            #print(tuple[0])
            if tuple[0] == self.start_stop.stop_id:
                self.start_stop_order = tuple[1]

            elif tuple[0] == self.dest_stop.stop_id:
                self.dest_stop_order = tuple[1]

        for tuple in self.stops_serviced:
            stop_order = tuple[1]
            #print(stop_order)
            #print(self.dest_stop_order)
            #print(self.start_stop_order)
            if stop_order <= self.dest_stop_order and stop_order >= self.start_stop_order:
                subroute.append(tuple)
        return subroute

    def get_number_stops_subroute(self):
        number_stops = len(self.subroute)
        return number_stops - 1

    def generate_stops_array(self, stop_list):
        stop_array = []
        #print("********")
        for stop_tuple in stop_list:
            #print(tuple)
            stop_dict = {}
            stop_id = stop_tuple[0]
            stop = BusStop.objects.get(stop_id = stop_id)

            stop_dict["stopId"] = stop_id
            stop_dict["stopName"] = stop.stop_name
            stop_dict["lat"] = stop.lat
            stop_dict["lng"] = stop.lng
            stop_dict["stopOrder"] = stop_tuple[1]

            stop_array.append(stop_dict)
        #print("END******")
        #print("Stops Dict",stop_array)
        return stop_array



def return_routes2(request):
    '''
    '''

    start_stop = request.GET['startstop']
    dest_stop = request.GET['endstop']

    start_stop = BusStop.objects.get(stop_id = start_stop)
    dest_stop = BusStop.objects.get(stop_id = dest_stop)

    start_stop_routes_serviced = start_stop.routes_serviced()
    #Dest stop sometimes returns NaN
    dest_stop_routes_serviced = dest_stop.routes_serviced()

    print("start stop", start_stop)
    print("dest stop", dest_stop)

    print("start routes serviced", start_stop_routes_serviced)
    print("dest routes serviced", dest_stop_routes_serviced)

    #common_routes = start_stop_routes_serviced.intersection(dest_stop_routes_serviced)
    common_routes = [route for route in start_stop_routes_serviced if route in dest_stop_routes_serviced]

    print("common routes", common_routes)

    list_of_lists = []
    temp_route_dict = {}

    data = []

    for route_id in common_routes:
        line_id = route_id.split("_")[0]
        temp_route_dict[route_id] = TempRoute(line_id, route_id, start_stop, dest_stop)
        #stop_list = TempRoute_dict[route].stops_serviced
        #stops = list(RouteStops.objects.values_list('stop_id', 'stop_order').filter(route_id = route))
        #stop_list += stops
        #list_of_lists.append(stop_list)
        temp_route_dict[route_id].print_route()
        temp_route_dict[route_id].print_subroute()
        temp_route_dict[route_id].print_lineID()
        temp_route_dict[route_id].print_number_stops()

        route_dict = {}
        route_dict["lineId"] = line_id
        route_dict["routeId"] = route_id
        route_dict["numberStops"] = temp_route_dict[route_id].number_stops
        route_dict["stopsServiced"] = temp_route_dict[route_id].stops_serviced_array
        route_dict["stopsServiced"] = temp_route_dict[route_id].subroute_stop_array

        data.append(route_dict)

    #print(data)
    #print({'routes_data':data})
    return JsonResponse({'routes_data': data})
