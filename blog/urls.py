from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.blog, name='blog'),
    # path('blog/', views.blog, name='blog'),
    path('posts/<int:post_id>/post_detail', views.post_detail, name='post_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


