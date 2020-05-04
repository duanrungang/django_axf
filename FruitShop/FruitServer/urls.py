from django.conf.urls import url

from FruitServer import views

urlpatterns = [
    url(r'^goodstype/', views.GoodsTypeAPIView.as_view(
        actions={
            "get": "get_goodstypes"
        }
    )),
    url(r'^goods/', views.GoodsAPIView.as_view(
        actions={
            "get": "list"
        }
    )),
    url(r'^orders/', views.OrderServerAPIView.as_view(
        actions={
            'post': 'handle_post'
        }
    ))
]
