
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
    def __init__(self, line_id, route_id, number_stops):
        self.line_id = line_id
        self.route_id = route_id
        #self.number_stops = number_stops

    def get_stop_list(self):
        self.stops_serviced = []


def return_routes2(request):
    '''
    '''

    start_stop = request.GET['startstop']
    dest_stop = request.GET['endstop']

    start_stop = BusStop.objects.get(stop_id = start_stop)
    dest_stop = BusStop.objects.get(stop_id = dest_stop)

    start_stop_routes_serviced = start_stop.routes_serviced()
    dest_stop_routes_serviced = dest_stop.routes_serviced()

    print("start", start_stop_routes_serviced)
    print("End", dest_stop_routes_serviced)

    #common_routes = start_stop_routes_serviced.intersection(dest_stop_routes_serviced)
    common_routes = [route for route in start_stop_routes_serviced if route in dest_stop_routes_serviced]

    print("common", common_routes)

    stop_list = []
    for route in common_routes:
        stops = list(RouteStops.objects.values_list('stop_id', 'stop_order').filter(route_id = route))
        stop_list += stops

    print(stop_list)

'''
    common_routes_info_dict = {}
    for common_route in common_routes:
        common_routes_info_dict[common_route] = Route(common_route, 11)

    for key in common_routes_info_dict:
        print("Key",key)
'''
