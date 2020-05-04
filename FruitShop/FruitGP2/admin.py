from django.contrib import admin

# Register your models here.
from FruitGP2.models import FruitUser, Cart, Order, OrderGoods, GoodsInfo, UserComments


class FruitUserAdmin(admin.ModelAdmin):
    list_display = ['f_name', 'f_age', 'f_sex', 'f_email', 'f_register_date']


class CartAdmin(admin.ModelAdmin):
    list_display = ['c_goods', 'c_user', 'c_goods_num', 'is_select']
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['o_user', 'o_status', 'o_price', 'o_order_time']


class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['o_order', 'o_goods_num']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['g_name', 'g_price', 'g_type', 'g_ordergoods']


class UserCommentsAdmin(admin.ModelAdmin):
    list_display = ['u_user', 'u_comment', 'u_comment_datetime', 'u_comment_add']


admin.site.register(FruitUser, FruitUserAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(UserComments, UserCommentsAdmin)
