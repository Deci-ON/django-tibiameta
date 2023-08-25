from django.urls import path
from . import views
from .views import sitemap
from django.views.generic.base import TemplateView



urlpatterns = [
    path('', views.index, name="index"),
    path("sitemap.xml", sitemap, name="sitemap"),
     path(
        "robots.txt",
        TemplateView.as_view(template_name="tibiameta/robots.txt", content_type="text/plain"),
    ),

]
