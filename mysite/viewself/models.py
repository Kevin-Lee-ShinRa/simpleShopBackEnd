from django.db import models

from django.test import TestCase
from django.db import models
# Create your tests here.


class Book(models.Model):  # 改为继承 Model 类
    title = models.CharField(max_length=100, verbose_name="书籍")
    price = models.IntegerField(verbose_name="价格")
    hub_date = models.DateField(verbose_name="日期")
    bread = models.IntegerField(verbose_name="阅读量")
    bcomment = models.IntegerField(verbose_name="评论量")
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE, verbose_name="出版社")
    authors = models.ManyToManyField("Author", verbose_name="作者")


class Publish(models.Model):  # 改为继承 Model 类
    name = models.CharField(max_length=100, verbose_name="出版社名称")
    email = models.EmailField(verbose_name="出版社邮箱")

    def __str__(self):
        return self.name


class Author(models.Model):  # 改为继承 Model 类
    name = models.CharField(max_length=100, verbose_name="作者")
    age = models.IntegerField(verbose_name="年龄")

    def __str__(self):
        return self.name

