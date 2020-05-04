from django.conf.urls import url

from DRF2 import views

urlpatterns = [
    url(r'index', views.hello),
    url(r'^getperson/', views.get_person),
    url(r'^addperson/', views.add_person),
    url(r'^getpersons/', views.get_persons),
    url(r'^hello/', views.HelloAPIView.as_view()),
    url(r'^persons/$', views.PersonsAPIView.as_view()),
    url(r'^persons/(?P<id>\d+)/', views.PersonAPIView.as_view()),
    url(r'^blogs/$', views.BlogsListAPIView.as_view()),
    url(r'^blogs/(?P<id>\d+)/$', views.BlogListAPIView.as_view()),
]
