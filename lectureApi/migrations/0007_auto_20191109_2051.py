# Generated by Django 2.2 on 2019-11-09 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectureApi', '0006_auto_20191109_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='length',
            field=models.IntegerField(choices=[(2, '二节课'), (1, '二节课'), (3, '三节课'), (4, '四节课')], verbose_name='持续时长'),
        ),
    ]