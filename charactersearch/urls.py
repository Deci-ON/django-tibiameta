from django.urls import path
from . import views   


urlpatterns = [ 
path('characterinfo/', views.characterinfo, name='characterinfo'),
]