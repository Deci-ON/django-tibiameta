"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("tibiameta.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('charactersearch/', include('charactersearch.urls')),
    path('lootsplit/', include('lootsplit.urls')),
    path('skillwheel/', include('skillwheel.urls')),
    path('topexp/', include('topexp.urls')),
    path('partylevelcalculator/', include('partylevelcalculator.urls')),
    path('expcalculator/', include('expcalculator.urls')),
    path('blog/', include('blog.urls')),
    path('exercisecalculator/', include('exercisecalculator.urls')),  
    path('worldsinfos/', include('worldsinfos.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
