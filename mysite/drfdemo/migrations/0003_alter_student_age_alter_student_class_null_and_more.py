# Generated by Django 5.0.7 on 2024-08-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfdemo', '0002_author_publish_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='student',
            name='class_null',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='班级编号'),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='姓名'),
        ),
    ]
