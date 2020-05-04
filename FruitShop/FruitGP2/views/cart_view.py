from rest_framework import viewsets, status
from rest_framework.response import Response

from FruitGP2.authentications import FruitUserTokenAuthentication
from FruitGP2.models import Cart
from FruitGP2.permissions import LoginPermission
from FruitGP2.serializers import CartSerializer


class CartAPIView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = FruitUserTokenAuthentication,
    permission_classes = LoginPermission,

    def handle_post(self, request, *args, **kwargs):
        action = request.query_params.get('action')

        if action == 'add_to_cart':
            return self.add_to_cart(request)
        elif action == 'goods_num_up':
            return self.goods_num_up(request)
        elif action == 'goods_num_down':
            return self.goods_num_down(request)
        elif action == 'goods_select':
            return self.goods_select(request)
        elif action == 'goods_all_select':
            return self.goods_all_select(request)
        elif action == 'goods_one_del':
            return self.goods_one_del(request)
        elif action == 'goods_many_del':
            return self.goods_many_del(request)
        else:
            return self.handle_unknown_action(request)

    # 加入购物车
    def add_to_cart(self, request):
        goods_id = request.data.get('goods_id')
        goods_num = request.data.get('goods_num')

        # 参数校验,如果校验很多建议分装模块
        # goods_id = int(goods_id)
        goods_num = int(goods_num)

        carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goods_id)
        if not carts.exists():
            cart = Cart()
            cart.c_goods_id = goods_id
            cart.c_goods_num = goods_num or 1
            cart.c_user = request.user
        else:
            cart = carts.first()
            cart.c_goods_num = cart.c_goods_num + goods_num
        cart.save()
        data = {
            'msg': 'add success',
            'status': status.HTTP_201_CREATED,
            'data': self.get_serializer(cart).data
        }
        return Response(data)

    # 数量增加
    def goods_num_up(self, request, *args, **kwargs):
        cart_id = request.data.get('cart_id')
        goods_num = request.data.get('goods_num')
        goods_num = int(goods_num)

        carts = Cart.objects.filter(c_user=request.user).filter(id=cart_id)
        if not carts.exists():
            data = {
                'msg': '请正确选择订单',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)

        cart = carts.first()
        cart.c_goods_num = cart.c_goods_num + goods_num
        cart.save()

        data = {
            'msg': '数量增加成功',
            'status': status.HTTP_200_OK,
            'data': self.get_serializer(cart).data
        }
        return Response(data)

    # 数量减少
    def goods_num_down(self, request):
        cart_id = request.data.get('cart_id')
        goods_num = request.data.get('goods_num')
        goods_num = int(goods_num)

        carts = Cart.objects.filter(c_user=request.user).filter(id=cart_id)
        if not carts.exists():
            data = {
                'msg': '请正确选择订单',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)

        cart = carts.first()
        cart.c_goods_num = cart.c_goods_num - goods_num
        if not cart.c_goods_num > 0:
            cart.delete()
        else:
            cart.save()

        data = {
            'msg': '数量减少成功',
            'status': status.HTTP_200_OK,
            'data': self.get_serializer(cart).data
        }
        return Response(data)

    # 选中
    def goods_select(self, request):
        cart_id = request.data.get('cart_id')
        cart_select = request.data.get('cart_is_select')

        cart = Cart.objects.filter(c_user=request.user).filter(id=cart_id).first()
        if not cart:
            data = {
                'msg': '请正确选择订单',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)

        cart.is_select = cart_select
        cart.save()

        data = {
            'status': status.HTTP_200_OK
        }
        return Response(data)

    # 单个删除
    def goods_one_del(self, request):
        cart_id = request.data.get('cart_id')
        cart = Cart.objects.filter(c_user=request.user).filter(id=cart_id).first()
        if not cart:
            data = {
                'msg': '请正确选择订单',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)

        cart.delete()
        data = {
            'status': status.HTTP_200_OK
        }
        return Response(data)

    # 批量删除
    def goods_many_del(self, request):
        is_many_del = request.data.get('is_many_del')
        is_select = request.data.get('is_select')

        carts = Cart.objects.filter(c_user=request.user).filter(is_select=is_select)
        if not carts.exists():
            data = {
                'msg': '请正确选择订单',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)

        if is_many_del == 'y':
            for cart in carts:
                cart.delete()

        data = {
            'msg': 'ok'
        }
        return Response(data)

    # 全选
    def goods_all_select(self, request):
        is_all_select = request.data.get('is_all_select')

        carts = Cart.objects.filter(c_user=request.user)
        if not carts.exists():
            data = {
                'msg': '请正确选择订单',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)

        if is_all_select == 'y':
            for cart in carts:
                cart.is_select = True
                cart.save()
        elif is_all_select == 'n':
            for cart in carts:
                cart.is_select = False
                cart.save()
        data = {
            'msg': 'ok'
        }
        return Response(data)

    def handle_unknown_action(self, request):
        data = {
            'msg': 'unknown action',
            'status': status.HTTP_400_BAD_REQUEST
        }
        return Response(data)
