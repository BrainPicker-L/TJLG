from django.db import models

# Create your models here.
class top_article_model(models.Model):
    title = models.CharField('标题',max_length=20)
    img = models.ImageField('轮播图图片',upload_to='img')
    detail = models.CharField('轮播图内容',max_length=500)

    class Meta:
        verbose_name = '顶部轮播图'
        verbose_name_plural = '顶部轮播图'