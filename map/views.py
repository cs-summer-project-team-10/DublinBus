from django.shortcuts import render
from .models import Marker
# Create your views here.
def display(request):
    markers = Marker.objects.all()
    return render(request, 'map/index.html', {'markers': markers})
