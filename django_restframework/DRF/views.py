from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from DRF.models import Book
from DRF.serializers import UserSerializer, GroupSerializer, BookSerializer


def index(request):
    data = {
        'status': 200,
        'msg': 'index',
    }
    return JsonResponse(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
