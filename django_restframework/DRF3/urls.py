from django.conf.urls import url

from DRF3 import views

urlpatterns = [
    url(r'users/$', views.UsersAPIView.as_view()),
    url(r'users/(?P<pk>\d+)/$', views.UserAPIView.as_view()),
    url(r'users1/$', views.UsersListAPIView.as_view()),

    url(r'users2/$', views.UsersUpdateAPIView.as_view(
        actions={
            'get': 'list',
        }
    )),
    url(r'users2/(?P<pk>\d+)/$', views.UsersUpdateAPIView.as_view(
        actions={
            'get': 'retrieve',
        }
    )),

    url(r'users3/$', views.UsersAllAPIView.as_view(
        actions={
            'get': 'list',
            'post': 'create',
        }
    )),
    url(r'users3/(?P<pk>\d+)/$', views.UsersAllAPIView.as_view(
        actions={
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
            'delete': 'destroy',
        }
    )),

    url(r'users4/$', views.UsersCreateAPIView.as_view()),
    url(r'blogs/$', views.BlogsAPIView.as_view()),
    url(r'blogs/(?P<pk>\d+)/$', views.BlogAPIView.as_view()),
]
