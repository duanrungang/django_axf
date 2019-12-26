
import django_filters

from orders.models import Order, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_SEND


class OrderFilter(django_filters.rest_framework.FilterSet):
    o_status = django_filters.CharFilter('o_status', method='filter_status')

    class Meta:
        model = Order
        fields = ['o_status']

    def filter_status(self, queryset, name, value):
        if value == 'not_pay':
            return queryset.filter(o_status=ORDER_STATUS_NOT_PAY)
        elif value == 'not_send':
            return queryset.filter(o_status=ORDER_STATUS_NOT_SEND)
        else:
            return queryset