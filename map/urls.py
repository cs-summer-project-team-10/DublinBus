from django.urls import path
from . import views

urlpatterns = [

    path('', views.Display, name='Display'),
    path('routes/', views.return_routes, name='return_routes'),
]
