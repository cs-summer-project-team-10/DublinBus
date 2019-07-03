from django.shortcuts import render
from .models import BusStop
from django.http import HttpResponse
from django.shortcuts import HttpResponse, render, redirect 
import json

# Create your views here.
def display(request):
    ''' Simple view that renders the index html template with all the bus stop information
        using Jinja2
    '''
    bus_stops = BusStop.objects.all()
    bus_stop_list = []
    for bus_stop in bus_stops:
        bus_stop_list.append((bus_stop.stat_number, bus_stop.name, bus_stop.lat, bus_stop.lng))
    return render(request, 'map/index.html', {'JSONdata': json.dumps(bus_stop_list)})



# # Below it the test code written by James Su, please feel free to modify or delete it if anyone needs that

def routes(request):
    
    startstop = request.GET['startstop']
    endstop = request.GET['endstop']
    routelane = "Success ! " + " Start:  " + startstop + ",   " + " End: " + endstop
    r = HttpResponse(routelane)
    return r
