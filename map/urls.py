from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name='display'),
    path('json', views.send_json, name='send_json'),
]
