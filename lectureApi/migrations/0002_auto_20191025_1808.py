# Generated by Django 2.2 on 2019-10-25 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectureApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='length',
            field=models.IntegerField(choices=[(3, '三节课'), (1, '二节课'), (2, '二节课'), (4, '四节课')], verbose_name='持续时长'),
        ),
    ]
