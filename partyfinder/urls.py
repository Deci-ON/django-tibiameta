from django.urls import path
from . import views   

urlpatterns = [ 
    path('', views.partyforms, name='searchparty'),
    
]

# Adicione as URLs para HTMX separadamente
htmx_urlpatterns = [ 
    path('partyfinder/htmx_search_player', views.htmx_search_player, name='htmx_search_player'),
    path('partyfinder/htmx_search_world', views.htmx_search_world, name='htmx_search_world'),
    path('partyfinder/calc_level_range/', views.calc_level_range, name='calc_level_range'), 
]


urlpatterns += htmx_urlpatterns
