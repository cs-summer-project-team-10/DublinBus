from django.urls import path
from . import views

urlpatterns = [
    path('', views.Display, name='Display'),
    path('json', views.send_json, name='send_json'),
    path('jdata', views.send_data, name='send_jdata'),
]
