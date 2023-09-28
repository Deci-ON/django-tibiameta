from django.urls import path
from . import views   


urlpatterns = [
    path('', views.loot_split, name='lootsplit'),
]