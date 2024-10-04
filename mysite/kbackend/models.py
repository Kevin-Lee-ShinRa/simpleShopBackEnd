from django.db import models
from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User  # 引入 Django 的用户模型


class Goods(models.Model):
    good_name = models.CharField(max_length=100)
    good_price = models.FloatField()
    good_description = models.CharField(max_length=100)
    good_image = models.ImageField(upload_to='images/%Y/%m', default="images/default.jpg", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 自动设置为创建日期

    # 添加上传者的外键
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_goods")

    def __str__(self):
        return f"{self.good_name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class Comment(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.goods.good_name}"


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    replier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.replier.username} on {self.comment.id}"


class Cart(models.Model):
    good_name = models.CharField(max_length=100)
    good_price = models.FloatField()
    good_image = models.ImageField(upload_to='images/%Y/%m', default="images/default.jpg", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 自动设置为创建日期

    def __str__(self):
        return self.good_name


class Orders(models.Model):
    good_name = models.CharField(max_length=100)
    good_price = models.FloatField()
    good_image = models.ImageField(upload_to='images/%Y/%m', default="images/default.jpg", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 自动设置为创建日期

    def __str__(self):
        return self.good_name


class History(models.Model):
    good_name = models.CharField(max_length=100)
    good_price = models.FloatField()
    good_image = models.ImageField(upload_to='images/%Y/%m', default="images/default.jpg", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 自动设置为创建日期

    def __str__(self):
        return self.good_name
