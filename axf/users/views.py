from django.core.cache import cache
from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from orders.models import Order, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_SEND
from users.models import AxfUser
from users.serializers import AXFUserSerializer, LoginSerializer, RegisterSerializer
from utils import errors, conn


class AuthView(viewsets.GenericViewSet,
               mixins.ListModelMixin):

    queryset = AxfUser.objects.all()
    serializer_class = AXFUserSerializer

    def list(self, request, *args, **kwargs):
        # 获取token值
        token = self.request.query_params.get('token')
        # 获取redis中缓存的用户id值
        user_id = cache.get(token)
        user = AxfUser.objects.filter(id=user_id).first()
        serializer = self.serializer_class(user)
        # 查询订单状态
        orders_not_pay = Order.objects.filter(o_user=user, o_status=ORDER_STATUS_NOT_PAY).count()
        orders_not_send = Order.objects.filter(o_user=user, o_status=ORDER_STATUS_NOT_SEND).count()

        res = {
            'user_info': serializer.data,
            'orders_not_pay_num': orders_not_pay,
            'orders_not_send_num': orders_not_send,
        }
        return Response(res)

    @list_route(methods=['POST'], serializer_class=LoginSerializer)
    def login(self, request):
        # 登录操作
        # 将请求的参数进行序列化，并且做校验
        serializer = self.serializer_class(data=request.data)
        result = serializer.is_valid(raise_exception=False)
        if not result:
            raise conn.ParamError({'code': 1004, 'msg': '请求参数校验失败'})
        # 实现注册
        data = serializer.login_data(serializer.data)
        return Response(data)

    @list_route(methods=['POST'], serializer_class=RegisterSerializer)
    def register(self, request):
        """
        注册操作
        """
        # 将请求的参数进行序列化，并且做校验
        serializer = self.serializer_class(data=request.data)
        result = serializer.is_valid(raise_exception=False)
        if not result:
            raise conn.ParamError({'code': 1004, 'msg': '请求参数校验失败'})
        # 实现注册
        data = serializer.register_data(serializer.data)
        return Response(data)








