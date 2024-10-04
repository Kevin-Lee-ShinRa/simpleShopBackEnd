from django.db import models


# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name="姓名",blank=True, null=True)
    sex = models.BooleanField(default=1, verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄", blank=True, null=True)
    class_null = models.CharField(max_length=5, verbose_name="班级编号", blank=True, null=True)
    # description = models.TextField(max_length=100, verbose_name="问自己")

    class Meta:
        db_table = 'tb_student'
