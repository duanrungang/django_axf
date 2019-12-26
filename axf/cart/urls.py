from django.urls import path
from rest_framework.routers import SimpleRouter

from cart.views import CartView, AliPayView

router = SimpleRouter()
router.register('cart', CartView)
router.register('alipay', AliPayView)

urlpatterns = router.urls
