import logging

from alipay import AliPay
from django.http import JsonResponse

from FruitShop.settings import ALIPAY_APPID, ALIPAY_PUBLIC_KEY, APP_PRIVATE_KEY
from .user_view import FruitUsersAPIView
from .cart_view import CartAPIView
from .order_view import OrdersAPIView


def pay_ali(request):
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
        total_amount=1000,
        subject='华为p30',
        return_url="https://localhost:8000",
        notify_url="https://localhost:8000",  # 可选, 不填则使用默认notify url
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return JsonResponse({'msg': pay_url})


def learn_log(request):
    logger = logging.getLogger('gp2_learn')
    logger.warning('!!so')
    logger.warning('!!this is warning')

    return JsonResponse({'msg': 'logging'})
