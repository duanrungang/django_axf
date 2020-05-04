import os
import random

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, ListView

from App.models import Blog, RequestLog, Student
from django_restframework.settings import BASE_DIR, MEDIA_URL_PREFIX


def index(request):
    return render(request, 'index.html')


class HelloView(View):
    msg = None

    def get(self, request):
        return HttpResponse('hello view %s' % self.msg)

    def post(self, request):
        return HttpResponse('post helloview')

    def put(self, request):
        return HttpResponse('put helloview')


class LoginView(TemplateView):
    template_name = 'login.html'


class BlogListView(ListView):
    # template_name = 'blogs.html'
    model = Blog


def guess(request):
    lucky_num = random.randrange(100)
    client_num = request.GET.get('client_num')
    try:
        if lucky_num == int(client_num):
            return HttpResponse('恭喜中奖了')
    except Exception as e:
        print(e)

    return HttpResponse('感谢支持，欢迎再次光临')


def search(request):
    key_words = request.GET.get('key')
    # 搜索 找到相关数据
    return HttpResponse('%s存在以下100个结果' % key_words)


# 分页
def get_log(request):
    p = int(request.GET.get('p', 1))

    logs = RequestLog.objects.all()
    pagenator = Paginator(logs, 5)
    page = pagenator.page(p)

    return render(request, 'logs.html', context=locals())


# 文件上传
class UploadView(TemplateView):
    template_name = 'up_load.html'

    def post(self, request):
        icon = request.FILES.get('icon')
        # icons_path = os.path.join(BASE_DIR, 'static/icons/%s' % icon.name)
        # with open(icons_path, 'wb') as icon_save:
        #     for part in icon.chunks():
        #         icon_save.write(part)
        #         icon_save.flush()

        username = request.POST.get('username')
        student = Student()
        student.s_name = username
        student.s_pic = icon
        student.save()

        return HttpResponse('上传成功')


# 获取头像
def get_icon(request):
    student = Student.objects.last()
    print(student.s_pic)
    print(student.s_pic.path)
    print(MEDIA_URL_PREFIX + student.s_pic.url)
    print(student.s_pic.size)

    return render(request, 'imageshow.html', context={'image_url': MEDIA_URL_PREFIX + student.s_pic.url})
