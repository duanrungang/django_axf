from django.urls import path
from rest_framework.routers import SimpleRouter

from goods.views import home, FoodTypeView, MarketView

router = SimpleRouter()
router.register('foodtype', FoodTypeView)
router.register('market', MarketView)

urlpatterns = [
    # 定义首页地址
    path('home/', home),
]
urlpatterns += router.urls
