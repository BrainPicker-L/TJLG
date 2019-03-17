# Generated by Django 2.1.7 on 2019-03-16 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=30, verbose_name='活动名')),
                ('title', models.CharField(max_length=30, verbose_name='题目（选填）')),
                ('speaker', models.CharField(max_length=30, verbose_name='主讲人')),
                ('host', models.CharField(max_length=30, verbose_name='主持人（选填）')),
                ('time', models.TimeField(verbose_name='时间')),
                ('start_time', models.IntegerField(choices=[(1, '第一节课'), (2, '第二节课'), (3, '第三节课'), (4, '第四节课'), (5, '第五节课'), (6, '第六节课'), (7, '第七节课'), (8, '第八节课'), (9, '第九节课')], verbose_name='开始时间')),
                ('length', models.IntegerField(choices=[(4, '四节课'), (3, '三节课'), (1, '二节课'), (2, '二节课')], verbose_name='持续时长')),
                ('location', models.CharField(max_length=50, verbose_name='地点')),
                ('intro', models.CharField(max_length=120, verbose_name='主讲人简介(选填)(最多120字)')),
            ],
        ),
    ]
