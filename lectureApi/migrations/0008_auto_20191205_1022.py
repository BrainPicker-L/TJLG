# Generated by Django 2.2 on 2019-12-05 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectureApi', '0007_auto_20191109_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='length',
            field=models.IntegerField(choices=[(4, '四节课'), (3, '三节课'), (2, '二节课'), (1, '二节课')], verbose_name='持续时长'),
        ),
    ]
