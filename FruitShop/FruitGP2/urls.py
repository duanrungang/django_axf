from django.conf.urls import url

from FruitGP2 import views

urlpatterns = [
    url(r'^users/$', views.FruitUsersAPIView.as_view(
        actions={
            'post': 'handle_post',
            "get": "handle_get",
        }
    )),
    # url(r'^users/(?P<pk>\d+)/$', views.FruitUserAPIView.as_view(
    #     actions={
    #
    #     }
    # )),
    url(r'^carts/$', views.CartAPIView.as_view(
        actions={
            'post': 'handle_post',
        }
    )),
    url(r'^orders/$', views.OrdersAPIView.as_view(
        actions={
            'post': 'handle_post',
        }
    )),
    url(r'^alipay/', views.pay_ali),
    url(r'^log/', views.learn_log),
]
