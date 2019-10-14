from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('autors/', views.about, name='autors'),
                  path('autor/', views.autor, name='autor'),
                  path('topic/1', views.simple_topic, name='topic_1'),
                  path('topic/', views.blog, name='topic'),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
