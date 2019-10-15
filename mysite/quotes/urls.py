from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('autors/', views.about, name='autors'),
    path('autor/', views.autor, name='autor'),
    path('topic/1', views.simple_topic, name='topic_1'),
    path('topic/', views.blog, name='topic'),
]


