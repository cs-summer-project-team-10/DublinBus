from django.shortcuts import render
from .models import BusStop
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
        bus_stop_list.append((bus_stop.stat_number, bus_stop.name, bus_stop.lat, bus_stop.lng))

    return JsonResponse({'JSONdata': bus_stop_list})
