from django.db import models


# Create your models here.
class User(models.Model):
    u_name = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)

    def verify_password(self, password):
        return self.u_password == password


class Blog(models.Model):
    b_title = models.CharField(max_length=32)
    b_content = models.TextField()
    b_author = models.ForeignKey(User)

