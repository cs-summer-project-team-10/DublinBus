from django.shortcuts import render
from .models import BusStop,RouteStops,Routes,LeaveTime,Trip,Vehicle
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

def return_id(num):
    route_stops = RouteStops.objects.filter(stopID=num)
    route_stops_list = []
    for route_stop in route_stops:
        route_stops_list.append(route_stop.routeID.routeID)
    return route_stops_list


def send_data(request):
    ''' Django API that will return the bus stop data as JSON data
    '''
    num1=2
    num2=19
    list1=return_id(num1)
    list2=return_id(num2)
    common = [val for val in list1 if val in list2]
    route_stops_order = []
    route_all_stops = []

    if len(common):
        for com_route in common:
            Rname=Routes.objects.get(routeID=com_route).routeName
            Rstops=RouteStops.objects.filter(routeID=com_route)
            for Rstop in Rstops:
                dict2 = {}
                dict2['stopid'] = Rstop.stopID.stat_number
                dict2['shortname']=BusStop.objects.get(stat_number=Rstop.stopID.stat_number).name
                dict2['latitude']=BusStop.objects.get(stat_number=Rstop.stopID.stat_number).lat
                dict2['longitude']=BusStop.objects.get(stat_number=Rstop.stopID.stat_number).lng
                dict2['stop_order']=Rstop.stop_order
                route_all_stops.append(dict2)
            dict={}
            dict['routeID']=com_route
            dict['routeName'] = Rname
            dict['stops'] =route_all_stops
            route_stops_order.append(dict)

        return JsonResponse({'commondata': route_stops_order})
    else:
        return JsonResponse({'commondata': route_stops_order})
        # return JsonResponse({'commondata': common})

    # return JsonResponse({'JSONdata': route_stops_list2})

