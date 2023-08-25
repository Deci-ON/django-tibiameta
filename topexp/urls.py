from django.urls import path
from . import views

urlpatterns = [
    path('', views.top100exp, name='top100exp'),
    path('search/', views.search, name='search'),
]
