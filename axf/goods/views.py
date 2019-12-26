
import json

from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from goods.filters import GoodsFilter
from goods.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods
from goods.serializers import MainWheelSerializer, MainNavSerializer, MainMustBuySerializer, MainShopSerializer, \
    MainShowSerializer, FoodTypeSerializer, GoodsSerializer
from utils.my_redis import myredis


@api_view(['GET'])
def home(request):
    # data = {}
    # TODO: 使用redis缓存数据
    # wheels = myredis.hget('home', 'main_wheels')
    # if wheels:
    #     data['main_wheels'] = json.loads(wheels)
    # else:
    #     main_wheels = MainWheel.objects.all()
    #     data = MainWheelSerializer(main_wheels, many=True).data
    #     # json.dumps()将字典数据转化为json数据
    #     # json.loads()将json数据转化为字典数据
    #     myredis.hset('home', 'main_wheels', json.dumps(data))
    #     data['main_wheels'] = json.loads(wheels)

    # 返回首页商品信息
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shows = MainShow.objects.all()
    # 返回首页商品的信息
    data = {
        "main_wheels": MainWheelSerializer(main_wheels, many=True).data,
        "main_navs": MainNavSerializer(main_navs, many=True).data,
        "main_mustbuys": MainMustBuySerializer(main_mustbuys, many=True).data,
        "main_shops": MainShopSerializer(main_shops, many=True).data,
        "main_shows": MainShowSerializer(main_shows, many=True).data
    }
    return Response(data)


class FoodTypeView(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    # 闪购超市分类信息
    queryset = FoodType.objects.all()
    serializer_class = FoodTypeSerializer


class MarketView(viewsets.GenericViewSet,
                 mixins.ListModelMixin):
    # 闪购超市商品信息
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        # 过滤出默认的商品信息
        order_rule_list = [
            {"order_name": "综合排序", "order_value": 0},
            {"order_name": "价格升序", "order_value": 1},
            { "order_name": "价格降序", "order_value": 2},
            {"order_name": "销量升序", "order_value": 3},
            {"order_name": "销量降序", "order_value": 4},
        ]
        # 商品分类信息
        typeid = self.request.query_params.get('typeid')
        foodtype = FoodType.objects.get(typeid=typeid)
        foodtypechildnames = foodtype.childtypenames
        foodtypechildname_list = foodtypechildnames.split("#")
        foodtype_childname_list = []
        for foodtypechildname in foodtypechildname_list:
            foodtype_childname = dict()
            foodtype_childname_split = foodtypechildname.split(":")
            foodtype_childname['child_name'] = foodtype_childname_split[0]
            foodtype_childname['child_value'] = foodtype_childname_split[1]
            foodtype_childname_list.append(foodtype_childname)

        res = {
            # 返回商品的列表信息
            'goods_list': serializer.data,
            # 返回过滤规则
            "order_rule_list": order_rule_list,
            # 返回商品小分类信息
            'foodtype_childname_list': foodtype_childname_list
        }
        return Response(res)
