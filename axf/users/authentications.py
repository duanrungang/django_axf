from django.core.cache import cache
from django_redis import get_redis_connection
from rest_framework.authentication import BaseAuthentication

from users.models import AxfUser
from utils import conn, errors
from utils.my_redis import myredis


class UserTokenAuthentications(BaseAuthentication):
    def authenticate(self, request):
        try:
            # 获取token参数
            token = request.data.get("token") if request.data.get("token") else request.query_params.get('token')
            user_id = cache.get(token)
            # # 使用散列hash进行存储，存储token值，用户的id，用户的登录时间
            # user_id = myredis.hget(token, 'user_id')

            user = AxfUser.objects.get(pk=user_id)
            return user, token
        except Exception as e:
            print("用户认证失败")
            raise conn.ParamError({'code': 1007, 'msg': '用户没有登录，无法操作'})
