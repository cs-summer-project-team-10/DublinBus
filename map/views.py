
from django.shortcuts import render, get_object_or_404
#from .models import BusStop,RouteStops,Routes,LeaveTime,Trip,Vehicle,TrackingRawData,Justification
from .models import BusStop,RouteStops, Routes
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, render, redirect
import json


# Create your views here.
def Display(request):
    ''' Simple view that renders the index html template with all the bus stop information
        using Jinja2
    '''
    bus_stops = BusStop.objects.all()
    bus_stop_list = []
    for bus_stop in bus_stops:
        bus_stop_list.append((bus_stop.stop_id, bus_stop.stop_name, bus_stop.lat, bus_stop.lng))
    return render(request, 'map/index.html', {'JSONdata': json.dumps(bus_stop_list)})



# # Below it the test code written by James Su, please feel free to modify or delete it if anyone needs that

def return_id(num):
   route_stops = RouteStops.objects.filter(stop_id=num)
   route_stops_list = []
   for route_stop in route_stops:
       route_stops_list.append(route_stop.route_id.route_id)
   return route_stops_list




def return_routes(request):
    ''' Django API that will return the bus stop data as JSON data
    '''
    num1 = request.GET['startstop']
    num2 = request.GET['endstop']
    list1 = return_id(num1)
    list2 = return_id(num2)
    common = [val for val in list1 if val in list2]
    route_stops_order = []
    route_all_stops = []

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
