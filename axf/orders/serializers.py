from rest_framework import serializers

from goods.serializers import GoodsSerializer
from orders.models import Order, OrderGoods


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "o_status", "o_time", "o_price")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        order_goods= instance.ordergoods_set.all()
        serializer = OrderGoodsSerializer(order_goods, many=True)
        data['order_goods_info'] = serializer.data
        return data


class OrderGoodsSerializer(serializers.ModelSerializer):
    o_goods = GoodsSerializer()
    class Meta:
        model = OrderGoods
        fields = '__all__'
