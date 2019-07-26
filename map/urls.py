from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_page, name='home_page'),
    path('routes/', views.return_routes, name='return_routes'),
    path('prices/', views.return_prices, name='return_prices'),
    path('predict/', views.predict, name='predict')
]
