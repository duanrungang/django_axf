from django.shortcuts import render
from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response

from FruitGP2.contants import ORDER_PAYED, ORDER_SEND
from FruitGP2.models import Order
from FruitGP2.serializers import OrderSerializer
from FruitServer.goods_sort_rule import PRICE_UP, PRICE_DOWN, sort_rules
from FruitServer.models import GoodsTypeOne, Goods
from FruitServer.serializers import TypeOneSerializer, GoodsSerializer


class GoodsTypeAPIView(viewsets.ModelViewSet):
    queryset = GoodsTypeOne.objects.all()
    serializer_class = TypeOneSerializer

    def get_goodstypes(self, request, *args, **kwargs):
        data = {
            "msg": "ok",
            "status": status.HTTP_200_OK,
            "sortrule": sort_rules,
            "types": self.list(request).data,
        }

        return Response(data)


class GoodsAPIView(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # 筛选  一级标识   二级标识（可选）  三级排序（可选）
        typeone = self.request.query_params.get("typeone")
        typetwo = self.request.query_params.get("typetwo")
        sortrule = self.request.query_params.get("sortrule")

        if not typeone:
            raise exceptions.APIException(detail="请提供正确的参数")

        queryset = queryset.filter(g_type__g_one_id=typeone)

        if typetwo:
            queryset = queryset.filter(g_type_id=typetwo)

        if sortrule == PRICE_UP:
            queryset = queryset.order_by("g_price")
            # 价格升序
        elif sortrule == PRICE_DOWN:
            queryset = queryset.order_by("-g_price")
            # 价格降序

        return queryset


class OrderServerAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer,

    def handle_post(self, request, *args, **kwargs):
        action = request.query_params.get("action")
        if action == 'send':
            return self.do_send(request)
        else:
            return self.handle_unknown_action(request)

    # 已发货
    def do_send(self, request):

        orders = Order.objects.all()
        for order in orders:
            if order.o_status == ORDER_PAYED:
                order.o_status = ORDER_SEND
                order.save()

        data = {
            'msg': '发货成功!!',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    def handle_unknown_action(self, request):

        data = {
            "msg": "unknown action",
            "status": status.HTTP_400_BAD_REQUEST
        }

        return Response(data)
