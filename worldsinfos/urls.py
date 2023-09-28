from django.urls import path
from . import views   


urlpatterns = [ 
path('', views.onopenpage, name='onopenpage'),
path('searchbyworld', views.searchbyworld, name='searchbyworld'),

]