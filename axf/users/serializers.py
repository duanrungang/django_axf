import uuid
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from rest_framework import serializers

from users.models import AxfUser
from utils import errors, conn
from utils.my_redis import myredis


class AXFUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AxfUser
        fields = ("id", "u_username", "u_password", "u_email")


class LoginSerializer(serializers.Serializer):
    # 登录序列化
    u_username = serializers.CharField()
    u_password = serializers.CharField(min_length=6, max_length=20, error_messages={
        'max_length': '密码不能超过20字符',
        'min_length': '密码不能短于6字符'
    })

    def validate(self, attrs):
        username = attrs.get('u_username')
        password = attrs.get('u_password')
        # 判断账号是否已经注册，如果没有注册，则抛出错误
        if not AxfUser.objects.filter(u_username=username).exists():
            raise conn.ParamError({'code': 1005, 'msg': '登录账号不存在，请更换账号再登录'})
        # 判断账号和密码是否正确
        user = AxfUser.objects.filter(u_username=username).first()
        if not check_password(password, user.u_password):
            raise conn.ParamError({'code': 1006, 'msg': '账号或密码错误，请确认登录信息'})
        return attrs

    def login_data(self, validate_data):
        # 实现登录功能
        user = AxfUser.objects.filter(u_username=validate_data['u_username']).first()
        token = uuid.uuid4().hex
        # 使用缓存cache
        cache.set(token, user.id, timeout=60 * 60 * 7 * 24)
        # # 使用散列hash进行存储，存储token值，用户的id，用户的登录时间
        # myredis.hset(token, 'user_id', user.id)
        # myredis.hset(token, 'login_time', datetime.now())

        res_data = {
            'msg': '请求成功',
            'user_id': user.id,
            'token': token
        }
        return res_data


class RegisterSerializer(serializers.Serializer):
    # 登录序列化
    u_username = serializers.CharField()
    u_password = serializers.CharField(min_length=6, max_length=20, error_messages={
        'max_length': '密码不能超过20字符',
        'min_length': '密码不能短于6字符'
    })
    u_password2 = serializers.CharField(min_length=6, max_length=20, error_messages={
        'max_length': '密码不能超过20字符',
        'min_length': '密码不能短于6字符'
    })
    u_email = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('u_username')
        password = attrs.get('u_password')
        password2 = attrs.get('u_password2')
        u_email = attrs.get('u_email')
        # 判断如果账号已存在则抛出错误提示
        if AxfUser.objects.filter(u_username=username).exists():
            raise conn.ParamError({'code': 1001, 'msg': '注册账号已存在，请更换账号'})
        # 判断密码和确认密码是否一致
        if password != password2:
            raise conn.ParamError({'code': 1002, 'msg': '注册密码和确认密码不一致'})
        # 校验邮箱是否已存在
        if AxfUser.objects.filter(u_email=u_email).exists():
            raise conn.ParamError({'code': 1003, 'msg': '邮箱已存在，请更换邮箱'})
        # 返回校验的参数
        return attrs

    def register_data(self, validate_data):
        # 注册操作
        u_password = make_password(validate_data['u_password'])
        user = AxfUser.objects.create(u_username=validate_data['u_username'],
                                      u_password=u_password,
                                      u_email=validate_data['u_email'])
        res_data = {
            'msg': '请求成功',
            'user_id': user.id
        }
        return res_data

