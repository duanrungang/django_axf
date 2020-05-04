from rest_framework import serializers

from FruitServer.models import GoodsTypeOne, GoodsTypeTwo, Goods


class TypeTwoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsTypeTwo
        fields = ["id", "g_name"]


class TypeOneSerializer(serializers.ModelSerializer):

    goodstypetwos = TypeTwoSerializer(many=True)

    class Meta:
        model = GoodsTypeOne
        fields = ["id", "g_name", "goodstypetwos"]


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = "__all__"
