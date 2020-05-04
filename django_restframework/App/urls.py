from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^hello/', views.HelloView.as_view(msg='hhh')),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^blog/', views.BlogListView.as_view(), name='blog'),
    url(r'^guess/', views.guess),
    url(r'^search/', views.search),
    url(r'^getlogs/', views.get_log),
    url(r'^upload/', views.UploadView.as_view(), name='upload'),  # 上传文件
    url(r'^geticon/', views.get_icon),

]
