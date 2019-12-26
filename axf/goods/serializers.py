
from rest_framework import serializers

from goods.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods


class MainWheelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainWheel
        fields = ("id", "img", "name", "trackid")


class MainNavSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainNav
        fields = ("id", "img", "name", "trackid")


class MainMustBuySerializer(serializers.ModelSerializer):

    class Meta:
        model = MainMustBuy
        fields = ("id", "img", "name", "trackid")


class MainShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainShop
        fields = ("id", "img", "name", "trackid")


class MainShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainShow
        fields = "__all__"


class FoodTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodType
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = "__all__"
