from django.db import models


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField(default=20)


class Department(models.Model):
    title = models.CharField(max_length=16)


# Department.objects.create(title="南草坪")
