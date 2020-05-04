from django.db import models


# Create your models here.
class Blog(models.Model):
    b_title = models.CharField(max_length=32)
    b_content = models.TextField()


class RequestLog(models.Model):
    r_ip = models.CharField(max_length=32)
    r_time = models.FloatField(default=0)


class Student(models.Model):
    s_name = models.CharField(max_length=16)
    s_pic = models.ImageField(upload_to='s_icons')
