from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_wheel, name='skillwheel'),
]
