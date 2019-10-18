from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='index'),
    path('autors/', views.about, name='autors'),
    path('autor/<slug:slug>', views.AutorView.as_view(), name='autor'),
    path('topic/1', views.simple_topic, name='topic_1'),
    path('topic/', views.blog, name='topic'),
]
