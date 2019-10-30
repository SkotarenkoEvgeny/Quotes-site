from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='index'),
    path('autors/', views.AutorListView.as_view(), name='autors'),
    path('autor/<slug:slug>', views.AutorView.as_view(), name='autor'),
    path('topic/<slug:slug>', views.SimpleTopicList.as_view(),
         name='topic_quotes'),
    path('topic/', views.TopicListView.as_view(), name='topic'),
    path('admin/contact_form', views.AdminContactView.as_view(), name='admin-contact'),
    path('search', views.SearchIndexView.as_view(), name='search')
]
