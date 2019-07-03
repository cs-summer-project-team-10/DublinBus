from django.urls import path
from . import views

urlpatterns = [

    path('', views.Display, name='Display'),
    path('jdata', views.send_data, name='send_jdata'),
# Below it the test code written by James Su, please feel free to modify or delete it if anyone needs that
    path('routes/', views.routes, name='routes'),
]
