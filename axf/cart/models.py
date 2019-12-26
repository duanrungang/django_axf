from django.db import models

from goods.models import Goods
from users.models import AxfUser


class Cart(models.Model):
    c_user = models.ForeignKey(AxfUser, on_delete=models.SET_NULL, null=True)
    c_goods = models.ForeignKey(Goods, on_delete=models.SET_NULL, null=True)

    c_goods_num = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'
