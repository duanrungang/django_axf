from django.db import models


# Create your models here.
class Person(models.Model):
    p_name = models.CharField(max_length=32, unique=True)
    p_age = models.IntegerField(default=1)


class Blog(models.Model):
    b_title = models.CharField(max_length=32)
    b_content = models.TextField()
