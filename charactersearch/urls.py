from django.urls import path
from . import views   


urlpatterns = [ 
path('', views.characterinfo, name='characterinfo'),
]