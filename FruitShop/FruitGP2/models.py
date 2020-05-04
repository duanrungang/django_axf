from django.contrib.auth.hashers import check_password
from django.db import models

# Create your models here.
from FruitServer.models import Goods, GoodsTypeTwo


class FruitUser(models.Model):
    f_name = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    f_password = models.CharField(verbose_name='密码', max_length=256)
    f_age = models.IntegerField(verbose_name='年龄', default=1)
    f_sex = models.BooleanField(verbose_name='性别', default=False)

    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    is_forbidden = models.BooleanField(default=False)
    f_email = models.CharField(verbose_name='邮箱', max_length=64, unique=True)
    f_register_date = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    f_icon = models.CharField(verbose_name='图片', max_length=128, null=True)

    is_active = models.BooleanField(default=False)

    def verify_password(self, password):
        return check_password(password, self.f_password)

    class Meta:
        verbose_name = '用户'

    def __str__(self):
        return self.f_name


class Cart(models.Model):
    c_user = models.ForeignKey(FruitUser, verbose_name='用户')
    c_goods = models.ForeignKey(Goods, verbose_name='商品')
    c_goods_num = models.IntegerField(default=1, verbose_name='商品数量')
    is_select = models.BooleanField(default=True, verbose_name='是否选中')

    def __str__(self):
        return self.c_goods

    class Meta:
        verbose_name = '购物车'


class Order(models.Model):
    o_user = models.ForeignKey(FruitUser, verbose_name='用户')
    o_status = models.IntegerField(default=0, verbose_name='等级')
    o_price = models.FloatField(default=0, verbose_name='总价')
    o_order_time = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    def __str__(self):
        return self.o_user

    class Meta:
        verbose_name = '订单'


class OrderGoods(models.Model):
    o_goods_num = models.IntegerField(default=1)
    o_order = models.ForeignKey(Order)

    class Meta:
        verbose_name = '订单商品'


class GoodsInfo(models.Model):
    g_name = models.CharField(verbose_name='货物名', max_length=64)
    g_price = models.FloatField(verbose_name='货物价格', default=0)
    g_market_price = models.FloatField(verbose_name='货物市场价格', default=0)
    g_unit = models.CharField(verbose_name='单位', max_length=32)
    g_detail = models.TextField(verbose_name='货物详情')
    g_img = models.CharField(verbose_name='货物图片', max_length=128)
    g_bar_code = models.CharField(verbose_name='条形码', max_length=64)
    g_store_num = models.IntegerField(verbose_name='库存量', default=10)
    g_type = models.ForeignKey(GoodsTypeTwo, verbose_name='货物类型')
    g_ordergoods = models.OneToOneField(OrderGoods)

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name = '商品信息'


class UserComments(models.Model):
    u_comment = models.CharField(verbose_name='评论内容', max_length=200)
    u_comment_datetime = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    u_comment_add = models.CharField(max_length=256, verbose_name='追加评价')
    u_user = models.ForeignKey(Order)

    class Meta:
        verbose_name = '用户评价'


class UserAddress(models.Model):
    a_user = models.ForeignKey(FruitUser)
    a_address = models.CharField(max_length=256)


class OrderAddress(models.Model):
    o_user = models.OneToOneField(Order)
    o_address = models.CharField(max_length=256)
