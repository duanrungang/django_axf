
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from cart.models import Cart
from orders.filters import OrderFilter
from orders.models import Order, OrderGoods
from orders.serializers import OrderSerializer
from users.authentications import UserTokenAuthentications


class OrdersView(viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (UserTokenAuthentications,)
    filter_class = OrderFilter

    def create(self, request):
        carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
        # 创建订单
        order = Order()
        order.o_user = request.user
        order.o_price = self.get_total_price(request)
        order.save()
        # 创建订单详情表信息
        for cart_obj in carts:
            ordergoods = OrderGoods()
            ordergoods.o_order = order
            ordergoods.o_goods_num = cart_obj.c_goods_num
            ordergoods.o_goods = cart_obj.c_goods
            ordergoods.save()
            # 删除购物车表中数据
            cart_obj.delete()
        data = {
            'order_id': order.id
        }
        return Response(data)

    def get_total_price(self, request):
        # 计算修改后的商品价格
        carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
        total = 0
        for cart in carts:
            total += cart.c_goods_num * cart.c_goods.price
        return "{:.2f}".format(total)
