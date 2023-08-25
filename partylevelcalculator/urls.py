from django.urls import path
from . import views   


urlpatterns = [ 
path('', views.partylevelcalculator, name='partylevelcalculator'),
]