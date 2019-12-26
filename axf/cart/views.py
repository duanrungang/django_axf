
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
from alipay import Alipay


from axf.settings import ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from cart.models import Cart
from cart.serializers import CartSerializer
from users.authentications import UserTokenAuthentications


class CartView(viewsets.GenericViewSet,
               mixins.ListModelMixin):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (UserTokenAuthentications,)

    def list(self, request, *args, **kwargs):
        # 购物车中商品的展示
        carts = Cart.objects.filter(c_user=request.user)
        is_all_select = carts.filter(c_is_select=True).exists()
        # 序列化购物车中的商品信息
        serializer = self.serializer_class(carts, many=True)
        res = {
            'title': '购物车',
            'is_all_select': is_all_select,
            'total_price': self.get_total_price(request),
            'carts': serializer.data
        }
        return Response(res)

    @list_route(methods=['POST'])
    def add_cart(self, request):
        goodsid = request.data.get("goodsid")
        carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
        # 判断如果商品存在数据库中，则修改商品的数量
        if carts.exists():
            cart_obj = carts.first()
            cart_obj.c_goods_num = cart_obj.c_goods_num + 1
        else:
            # 如果商品不存在，则新增
            cart_obj = Cart()
            cart_obj.c_goods_id = goodsid
            cart_obj.c_user = request.user
        cart_obj.save()
        res = {
            'c_goods_num': cart_obj.c_goods_num
        }
        return Response(res)

    @list_route(methods=['POST'])
    def sub_cart(self, request):
        goodsid = request.data.get("goodsid")
        cart_obj = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid).first()

        if cart_obj.c_goods_num > 1:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            cart_obj.save()
            c_goods_num = cart_obj.c_goods_num
        else:
            cart_obj.delete()
            c_goods_num = 0
        res = {
            'c_goods_num': c_goods_num,
            'total_price': self.get_total_price(request)
        }
        return Response(res)

    def get_total_price(self, request):
        # 计算修改后的商品价格
        carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
        total = 0
        for cart in carts:
            total += cart.c_goods_num * cart.c_goods.price
        return "{:.2f}".format(total)


class AliPayView(viewsets.GenericViewSet,
                 mixins.ListModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @list_route(methods=['GET'])
    def pay(self, request):
        # 构建支付的科幻  AlipayClient
        alipay_client = Alipay(
            pid=ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=APP_PRIVATE_KEY,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA",  # RSA 或者 RSA2
            debug=False  # 默认False
        )
        # 使用Alipay进行支付请求的发起

        subject = "i9 20核系列 RTX2080"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay_client.api_alipay_trade_page_pay(
            out_trade_no="110",
            total_amount=10000,
            subject=subject,
            return_url="http://www.1000phone.com",
            notify_url="http://www.1000phone.com"  # 可选, 不填则使用默认notify url
        )

        data = {
            "msg": "ok",
            "status": 200,
            "data": {
                "pay_url": "https://openapi.alipaydev.com/gateway.do?" + order_string
            }
        }

        return Response(data)

    @list_route(methods=['POST'])
    def payed(self, request):
        # 支付
        pass

