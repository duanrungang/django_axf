from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status, exceptions
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from DRF2.models import Person, Blog
from DRF2.serializers import PersonSerializer, BlogSerializer


@api_view(['GET', 'POST'])
def hello(request):
    response = Response('index')
    return response
    # return HttpResponse('index')


def get_person(request):
    person = Person.objects.first()
    # 将对象转换为  字典 json格式
    serializer = PersonSerializer(person)
    data = {
        'msg': 'ok',
        'status': 200,
        'data': serializer.data
    }

    return JsonResponse(data)


def add_person(request):
    p_name = request.POST.get('p_name')
    p_age = request.POST.get('p_age')
    # person = Person()
    # person.p_name = p_name
    # person.p_age = p_age
    # person.save()
    # serializer = PersonSerializer(person)
    # data = {
    #     'msg': 'ok',
    #     'status': 200,
    #     'data': serializer.data
    # }
    person_data = {
        'p_name': p_name,
        'p_age': p_age,
    }
    serializer = PersonSerializer(data=person_data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors)
    serializer.save()
    data = {
        'msg': 'ok',
        'status': status.HTTP_201_CREATED,
        'data': serializer.data
    }
    return JsonResponse(data)


def get_persons(request):
    persons = Person.objects.all()
    serializer = PersonSerializer(persons, many=True)
    data = {
        'msg': 'ok',
        'status': 200,
        'data': serializer.data
    }

    return JsonResponse(data)


class HelloAPIView(APIView):
    def get(self, request):
        data = {
            'msg': 'ok',
        }
        return Response(data)


# 复数接口
class PersonsAPIView(APIView):
    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        p_name = request.data.get('p_name')
        p_age = request.data.get('p_age')
        person_info = {
            'p_name': p_name,
            'p_age': p_age,
        }
        serializer = PersonSerializer(data=person_info)

        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()

        return Response(serializer.data)


# 单数接口
class PersonAPIView(APIView):
    def get_object(self, id):
        try:
            person = Person.objects.get(pk=id)
            return person
        except Exception as e:
            raise exceptions.NotFound()

    def get(self, request, id):
        person = self.get_object(id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request):
        pass

    def patch(self, request):
        pass

    def delete(self, request):
        person = self.get_object(id)
        person.delete()
        data = {
            'msg': '删除成功',
            'status': 204,
        }
        return Response(data)


class BlogsListAPIView(GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class BlogListAPIView(GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
