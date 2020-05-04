import random
from time import time

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from App.models import RequestLog


class LearnMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 访问追踪  日志
        print(request.META.get('REMOTE_ADDR'), request.path, time())

        ip = request.META.get('REMOTE_ADDR')
        if request.path == '/app/guess/':
            if ip == '10.0.102.144':
                if random.randrange(100) > 10:
                    return HttpResponse('恭喜中了500w')

        if request.path == '/app/search/':
            if RequestLog.objects.filter(r_ip=ip).exists():
                rl = RequestLog.objects.filter(r_ip=ip).last()
                if time() - rl.r_time <= 10:
                    return HttpResponse('访问过于频繁请稍后再试')
            else:
                rl = RequestLog()
            rl.r_time = time()
            rl.r_ip = ip
            rl.save()
