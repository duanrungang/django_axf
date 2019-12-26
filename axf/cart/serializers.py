
from rest_framework import serializers

from cart.models import Cart
from goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):
    # 关联商品
    c_goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = ("id", "c_is_select", "c_goods_num", "c_goods")
