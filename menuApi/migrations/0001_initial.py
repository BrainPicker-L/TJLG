# Generated by Django 2.1.7 on 2019-03-20 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diningRoom', models.CharField(max_length=20, verbose_name='食堂')),
                ('winNum', models.CharField(max_length=20, verbose_name='窗口')),
                ('namePrice', models.CharField(max_length=100, verbose_name='菜品名称/价格')),
            ],
            options={
                'verbose_name': '食堂菜单内容',
                'verbose_name_plural': '食堂菜单内容',
            },
        ),
    ]
