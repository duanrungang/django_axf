import uuid

from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from DRF3.authentication import TokenAuthentication
from DRF3.models import User, Blog
from DRF3.permissions import UserLoginPermission
from DRF3.serializers import UserSerializer, BlogSerializer
from DRF3.throttlings import TenPerMinuteThrottle


class UsersAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersUpdateAPIView(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersAllAPIView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        if action == 'register':
            return self.do_register(request, *args, **kwargs)
        elif action == 'login':
            return self.do_login(request, *args, **kwargs)
        else:
            return self.no_action(request, *args, **kwargs)

    def do_register(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def do_login(self, request, *args, **kwargs):
        u_name = request.data.get('u_name')
        u_password = request.data.get('u_password')
        users = User.objects.filter(u_name=u_name)
        if not users.exists():
            raise exceptions.NotFound()
        user = users.first()
        if not user.verify_password(u_password):
            raise exceptions.ValidationError(detail='password error')

        token = uuid.uuid4().hex
        cache.set(token, user, 60 * 60 * 24 * 7)
        data = {
            'msg': 'ok',
            'status': 200,
            'token': token,
        }
        return Response(data)

    def no_action(self, request, *args, **kwargs):
        raise exceptions.ValidationError(detail='error action')


class BlogsAPIView(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = TokenAuthentication,
    permission_classes = UserLoginPermission,

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(b_author=self.request.user)


class BlogAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = TokenAuthentication,
    permission_classes = UserLoginPermission,
    throttle_classes = TenPerMinuteThrottle,
