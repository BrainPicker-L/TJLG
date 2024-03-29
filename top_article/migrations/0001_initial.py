# Generated by Django 2.2 on 2019-10-24 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='top_article_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('img', models.ImageField(upload_to='img', verbose_name='轮播图图片')),
                ('detail', models.CharField(max_length=500, verbose_name='轮播图内容')),
            ],
            options={
                'verbose_name': '顶部轮播图',
                'verbose_name_plural': '顶部轮播图',
            },
        ),
    ]
