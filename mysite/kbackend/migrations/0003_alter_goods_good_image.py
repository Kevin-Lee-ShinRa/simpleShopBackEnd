# Generated by Django 5.0.7 on 2024-08-22 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbackend', '0002_alter_goods_good_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='good_image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/%Y/%m'),
        ),
    ]
