# Generated by Django 2.2 on 2019-11-09 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectureApi', '0005_auto_20191109_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='length',
            field=models.IntegerField(choices=[(3, '三节课'), (4, '四节课'), (1, '二节课'), (2, '二节课')], verbose_name='持续时长'),
        ),
    ]