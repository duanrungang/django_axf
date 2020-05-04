from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication


class FruitUserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.query_params.get('token')
            user = cache.get(token)

            if user:
                return user, token
        except Exception as e:
            print(e, 'FruitUserTOken 认证失败')
