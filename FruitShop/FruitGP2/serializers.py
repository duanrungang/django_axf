from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from FruitGP2.models import FruitUser, Cart, Order, OrderGoods, GoodsInfo, UserComments, UserAddress, OrderAddress


class FruitUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password_hash = make_password(validated_data.get('f_password'))
        validated_data['f_password'] = password_hash
        return super().create(validated_data)

    class Meta:
        model = FruitUser
        fields = ['id', 'f_name', 'f_age', 'f_sex', 'f_email', 'f_register_date', 'f_icon']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'c_user', 'c_goods', 'c_goods_num', 'is_select']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'o_status', 'o_order_time', 'o_price']


class OrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGoods
        fields = ['id', 'o_goods_num']


class GoodsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsInfo
        fields = '__all__'


class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComments
        fields = ['u_comment', 'u_comment_datetime', 'u_comment_add', 'u_user']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['a_user', 'a_address']


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = ['o_user', 'o_address']
