from django.urls import path
from rest_framework.routers import SimpleRouter

from orders.views import OrdersView

router = SimpleRouter()
router.register('orders', OrdersView)

urlpatterns = router.urls
