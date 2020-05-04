from alipay import AliPay
from rest_framework import viewsets, status
from rest_framework.response import Response

from FruitGP2.authentications import FruitUserTokenAuthentication
from FruitGP2.contants import ORDER_PAYED, ORDER_RECEIVED, ORDER_SEND, ORDER_COMMENTED_NOT_ADD, ORDER_ORDERED
from FruitGP2.models import Order, Cart, OrderGoods, GoodsInfo, UserComments, FruitUser, UserAddress, OrderAddress
from FruitGP2.permissions import LoginPermission
from FruitGP2.serializers import OrderSerializer, UserCommentsSerializer
from FruitGP2.utils import get_total_price
from FruitShop.settings import ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY


class OrdersAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer, UserCommentsSerializer,
    authentication_classes = FruitUserTokenAuthentication,
    permission_classes = LoginPermission,

    def handle_post(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == "ordered":
            return self.do_ordered(request)
        elif action == 'add_address':
            return self.add_address(request)
        elif action == "payed":
            return self.do_payed(request)
        elif action == 'received':
            return self.do_received(request)
        elif action == 'commented':
            return self.do_commented(request)
        elif action == 'add_comment':
            return self.do_add_comment(request)
        else:
            return self.handle_unknown_action(request)

    # 填写用户地址
    def add_address(self, request):
        add_address = request.data.get('address')
        user = FruitUser.objects.filter(f_name=request.user).first()
        if not user:
            data = {
                "msg": "no user select",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)
        addr = UserAddress.objects.filter(a_address=add_address).first()
        if addr:
            data = {
                "msg": "地址已经存在!!!",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)
        addr = UserAddress()
        addr.a_user = user
        addr.a_address = add_address
        addr.save()
        data = {
            'msg': '地址添加成功',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    # 已下单未付款
    def do_ordered(self, request):
        # 选择地址
        addr = request.data.get('addr')

        # 选择用户的地址
        u_addr = UserAddress.objects.filter(a_user=request.user).filter(a_address=addr)
        if not u_addr.exists():
            data = {
                "msg": "地址不存在!!!",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)

        # 点击提交的时候   将用户购物车数据表中的选中的数据获取出来，生成订单
        order = Order()
        order.o_user = request.user
        order.o_price = get_total_price(request.user)
        order.save()

        carts = Cart.objects.filter(c_user=request.user).filter(is_select=True)

        if not carts.exists():
            data = {
                "msg": "no goods select",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)

        for cart in carts:
            ordergoods = OrderGoods()
            ordergoods.o_order = order
            ordergoods.o_goods_num = cart.c_goods_num
            ordergoods.save()

            goods = cart.c_goods
            goodsinfo = GoodsInfo()

            goodsinfo.g_price = goods.g_price
            goodsinfo.g_name = goods.g_name
            goodsinfo.g_bar_code = goods.g_bar_code
            goodsinfo.g_detail = goods.g_detail
            goodsinfo.g_img = goods.g_img
            goodsinfo.g_market_price = goods.g_market_price
            goodsinfo.g_store_num = goods.g_store_num
            goodsinfo.g_type = goods.g_type
            goodsinfo.g_unit = goods.g_unit
            goodsinfo.g_ordergoods = ordergoods
            goodsinfo.save()
            cart.delete()

        # 保存订单地址
        orderaddress = OrderAddress()
        orderaddress.o_user = order
        orderaddress.o_address = addr
        orderaddress.save()

        data = {
            "msg": "ordered success",
            "status": status.HTTP_201_CREATED
        }

        return Response(data)

    # 已付款未发货
    def do_payed(self, request):
        # 将生成的订单进行付款
        # o_price = Order.objects.get('o_price')
        is_pay = request.data.get('is_pay')

        orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_ORDERED)

        if not orders.exists():
            data = {
                "msg": "no order select",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)

        o_price_total = 0
        for order in orders:
            o_price_total += order.o_price

        # goods = GoodsInfo.objects.filter()

        if not is_pay == 'y':
            data = {
                'msg': '订单支付已取消',
                'status': status.HTTP_200_OK
            }
            return Response(data)

        # 支付
        alipay = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=APP_PRIVATE_KEY,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,
            sign_type="RSA",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no="20161112",
            total_amount=o_price_total,
            subject='商品总价为:',
            return_url="https://localhost:8000",
            notify_url="https://localhost:8000",  # 可选, 不填则使用默认notify url
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

        for order in orders:
            order.o_status = ORDER_PAYED
            order.save()

        data = {
            'msg': '支付成功',
            'url': pay_url,
        }
        return Response(data)

    # 已收货未评论
    def do_received(self, request):
        # 收到货物
        is_receive = request.data.get('is_receive')
        orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_SEND)

        if not orders.exists():
            data = {
                "msg": "no order select",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)

        if not is_receive == 'y':
            return Response({'msg': '取消确认收获'})

        for order in orders:
            order.o_status = ORDER_RECEIVED
            order.save()

        data = {
            'msg': '已经收货',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    # 已评论未追加评论
    def do_commented(self, request):
        user_order_id = request.data.get('id')
        user_comment = request.data.get('comment')
        orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_RECEIVED).filter(id=user_order_id)
        if not orders.exists():
            data = {
                "msg": "no order select",
                "status": status.HTTP_409_CONFLICT
            }
            return Response(data)
        order = orders.first()

        comment = UserComments()
        comment.u_user = order
        comment.u_comment = user_comment
        comment.save()

        order.o_status = ORDER_COMMENTED_NOT_ADD
        order.save()

        data = {
            'msg': '评论成功!!',
            'status': status.HTTP_200_OK,
            # 'comment': self.get_serializer(comment).data
        }
        return Response(data)

    # 追加评论
    def do_add_comment(self, request):
        comment_id = request.data.get('id')
        add_comment = request.data.get('add_comment')
        order = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_COMMENTED_NOT_ADD).filter(
            id=comment_id).first()
        if not order:
            data = {
                "msg": "no order select",
                "status": status.HTTP_409_CONFLICT
            }
            return Response(data)

        comment = UserComments.objects.filter(u_user=order).first()
        comment.u_comment_add = add_comment
        comment.save()
        data = {
            'msg': '追评成功!!!',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    def handle_unknown_action(self, request):

        data = {
            "msg": "unknown action",
            "status": status.HTTP_400_BAD_REQUEST
        }

        return Response(data)
