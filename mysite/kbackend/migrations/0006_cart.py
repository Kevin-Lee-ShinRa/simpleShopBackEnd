# Generated by Django 5.0.7 on 2024-08-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbackend', '0005_remove_goods_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_name', models.CharField(max_length=100)),
                ('good_price', models.FloatField()),
                ('good_image', models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/%Y/%m')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
