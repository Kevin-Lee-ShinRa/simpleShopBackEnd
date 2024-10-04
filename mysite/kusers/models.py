from django.db import models
from django.db import models

from django.contrib.auth.models import User  # 引入 Django 的内置用户模型
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from kbackend.models import Goods


# Create your models here.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 其他扩展字段
    avatar = models.ImageField(upload_to='images/avatar/%Y/%m', default='images/default.jpg', null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    nickname = models.CharField(max_length=50, blank=True, null=True)  # 新增昵称字段

    def __str__(self):
        return self.user.username


# 购物车模型
class UserCart(models.Model):
    good_name = models.CharField(max_length=100)
    good_price = models.FloatField()
    good_description = models.CharField(max_length=100, default='No description available')
    good_image = models.ImageField(upload_to='images/uesrcart/%Y/%m', default="images/default1.jpg", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.good_name} ({self.quantity} items)"


class UserHistory(models.Model):
    good_name = models.CharField(max_length=100)
    good_price = models.FloatField()
    good_description = models.CharField(max_length=100, default='No description available')
    good_image = models.ImageField(upload_to='images/uesrcart/%Y/%m', default="images/default1.jpg", null=True, blank=True)
    # quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.good_name} (items)"

# 订单模型
class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ManyToManyField(Goods, through='UserOrderItem')
    created_at = models.DateTimeField(auto_now_add=True)


class UserOrderItem(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# 评论模型
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 评论了 {self.goods.good_name}"
