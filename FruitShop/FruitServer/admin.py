from django.contrib import admin

# Register your models here.
from FruitServer.models import GoodsTypeOne, GoodsTypeTwo, Goods


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['g_name', 'g_price', 'g_market_price', 'g_store_num']
    list_per_page = 10
    list_filter = ['g_type']
    search_fields = ['g_name']


admin.site.register(GoodsTypeOne)
admin.site.register(GoodsTypeTwo)
admin.site.register(Goods, GoodsAdmin)
