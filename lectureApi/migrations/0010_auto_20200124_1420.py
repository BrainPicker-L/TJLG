# Generated by Django 2.2 on 2020-01-24 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectureApi', '0009_auto_20191205_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='length',
            field=models.IntegerField(choices=[(2, '二节课'), (1, '二节课'), (3, '三节课'), (4, '四节课')], verbose_name='持续时长'),
        ),
    ]
