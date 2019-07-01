from django.shortcuts import render
from .models import BusStop,RouteStops,Routes,LeaveTime,Trip,Vehicle,TrackingRawData,Justification
from django.http import JsonResponse

# Create your views here.
def display(request):
    ''' Simple view that renders the index html template with all the bus stop information
        using Jinja2
    '''
    bus_stops = BusStop.objects.all()
    return render(request, 'map/index.html', {'bus_stops': bus_stops})


def send_json(request):
    ''' Django API that will return the bus stop data as JSON data
    '''

    bus_stops = BusStop.objects.all()
    bus_stop_list = []
    for bus_stop in bus_stops:
        bus_stop_list.append((bus_stop.stat_number, bus_stop.name, bus_stop.lat, bus_stop.long))

    return JsonResponse({'JSONdata': bus_stop_list})




def send_data(request):
    ''' Django API that will return the bus stop data as JSON data
    '''
    route_stops=RouteStops.objects.filter(stopID=18)

    route_stops_list = []
    for route_stop in route_stops:
        route_stops_list.append(route_stop.routeID.routeID)

    return JsonResponse({'JSONdata': route_stops_list})