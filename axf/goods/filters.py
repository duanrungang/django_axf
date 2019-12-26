
import django_filters

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    # 过滤字段
    typeid = django_filters.CharFilter(name='categoryid')
    childcid = django_filters.CharFilter(method='filter_childcid')
    order_rule = django_filters.CharFilter(name='order_rule', method='filter_order_rule')

    class Meta:
        model = Goods
        fields = ['categoryid']

    def filter_order_rule(self, queryset, name, value):
        """
            {"order_name": "综合排序", "order_value": 0},
            {"order_name": "价格升序", "order_value": 1},
            {"order_name": "价格降序", "order_value": 2},
            {"order_name": "销量升序", "order_value": 3},
            {"order_name": "销量降序", "order_value": 4},
        """
        if value == '0':
            return queryset
        elif value == '1':
            return queryset.order_by("price")
        elif value == '2':
            return queryset.order_by("-price")
        elif value == '3':
            return queryset.order_by("productnum")
        elif value == '4':
            return queryset.order_by("-productnum")

    def filter_childcid(self, queryset, name, value):
        # 如果childcid为0，则表示过滤全部的大分类下的商品信息
        if value == '0':
            return queryset
        return queryset.filter(childcid=value)
