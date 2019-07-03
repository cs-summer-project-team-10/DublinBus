from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name='display'),
# Below it the test code written by James Su, please feel free to modify or delete it if anyone needs that
    path('routes/', views.routes, name='routes'),
]
