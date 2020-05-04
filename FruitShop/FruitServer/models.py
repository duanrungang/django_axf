from django.db import models


class GoodsTypeOne(models.Model):
    g_name = models.CharField(verbose_name='一级名单', max_length=32, unique=True)

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name = '一级目录'


class GoodsTypeTwo(models.Model):
    g_name = models.CharField(verbose_name='二级名单', max_length=32)
    g_one = models.ForeignKey(GoodsTypeOne, related_name="goodstypetwos")

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name = '二级目录'


class Goods(models.Model):
    g_name = models.CharField(verbose_name='货物名', max_length=64)
    g_price = models.FloatField(verbose_name='货物价格', default=0)
    g_market_price = models.FloatField(verbose_name='货物市场价格', default=0)
    g_unit = models.CharField(verbose_name='单位', max_length=32)
    g_detail = models.TextField(verbose_name='货物详情')
    g_img = models.CharField(verbose_name='货物图片', max_length=128)
    g_bar_code = models.CharField(verbose_name='条形码', max_length=64)
    g_store_num = models.IntegerField(verbose_name='库存量', default=10)
    g_type = models.ForeignKey(GoodsTypeTwo, verbose_name='货物类型')

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name = '商品名录'
