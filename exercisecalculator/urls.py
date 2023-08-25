from django.urls import path
from . import views

urlpatterns = [
    path('', views.exercisecalculator, name='exercisecalculator'),
    path("load_skills/", views.load_skills, name="load_skills"),
    path("exerciseresult/", views.exerciseresult, name="exerciseresult"),

]
