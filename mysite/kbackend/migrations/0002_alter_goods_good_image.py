# Generated by Django 5.0.7 on 2024-08-22 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbackend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='good_image',
            field=models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/%Y/%m'),
        ),
    ]
