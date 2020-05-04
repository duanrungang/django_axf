from django.conf.urls import url
from rest_framework import routers

from DRF import views
from DRF.views import BookViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register('books', BookViewSet)

urlpatterns = [
    url(r'^index/', views.index),
]
