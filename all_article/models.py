from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField("标题",max_length=50)
    detail_url = models.URLField("文章详情链接--(可选)(注:只能添加已关联公众号文章链接或通过本网站发布的详情文章链接):",null=True,default="",blank=True)
    excerpt = models.TextField("摘要")
    created_time = models.DateTimeField(auto_now_add=False)
    last_updated_time = models.DateTimeField(auto_now=False)
    img1 = models.ImageField("图片1",upload_to='img',null=True,default="",blank=True)
    img2 = models.ImageField("图片2",upload_to='img',null=True,default="",blank=True)
    img3 = models.ImageField("图片3",upload_to='img',null=True,default="",blank=True)
    img4 = models.ImageField("图片4",upload_to='img',null=True,default="",blank=True)
    img5 = models.ImageField("图片5",upload_to='img',null=True,default="",blank=True)
    img6 = models.ImageField("图片6",upload_to='img',null=True,default="",blank=True)
    img7 = models.ImageField("图片7",upload_to='img',null=True,default="",blank=True)
    img8 = models.ImageField("图片8",upload_to='img',null=True,default="",blank=True)
    img9 = models.ImageField("图片9",upload_to='img',null=True,default="",blank=True)
    class Meta:
        verbose_name = '社团动态（天津理工）'
        verbose_name_plural = '社团动态（天津理工）'

class TJLG_Article_Pyspider(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField("标题",max_length=50)
    detail_url = models.URLField("文章详情链接--(可选)(注:只能添加已关联公众号文章链接或通过本网站发布的详情文章链接):",null=True,default="",blank=True)
    excerpt = models.TextField("摘要")
    created_time = models.DateTimeField(auto_now_add=False)
    last_updated_time = models.DateTimeField(auto_now=False)
    img1 = models.ImageField("图片1",upload_to='img',null=True,default="",blank=True)
    img2 = models.ImageField("图片2",upload_to='img',null=True,default="",blank=True)
    img3 = models.ImageField("图片3",upload_to='img',null=True,default="",blank=True)
    img4 = models.ImageField("图片4",upload_to='img',null=True,default="",blank=True)
    img5 = models.ImageField("图片5",upload_to='img',null=True,default="",blank=True)
    img6 = models.ImageField("图片6",upload_to='img',null=True,default="",blank=True)
    img7 = models.ImageField("图片7",upload_to='img',null=True,default="",blank=True)
    img8 = models.ImageField("图片8",upload_to='img',null=True,default="",blank=True)
    img9 = models.ImageField("图片9",upload_to='img',null=True,default="",blank=True)
    class Meta:
        verbose_name = '教务通知（天津理工）'
        verbose_name_plural = '教务通知（天津理工）'



class Email(models.Model):
    title = models.CharField("标题",max_length=50)
    ask = models.CharField("问题",max_length=2000)
    answer=models.CharField("回答",max_length=2000)
    create_time = models.DateTimeField(auto_now_add=False)









class SchoolLife(models.Model):
    author_name = models.CharField('作者名',max_length=20)
    avatar = models.ImageField('作者头像',upload_to='user_avatar',null=True, default="", blank=True)
    weixin_link = models.CharField('推文连接',max_length=100)
    background_img = models.ImageField('背景图',upload_to='weixin_background_img',null=True, default="", blank=True)

class AhuAdvert(models.Model):
    weixin_link = models.CharField('推文连接',max_length=100)
    background_img = models.ImageField('背景图',upload_to='weixin_background_img',null=True, default="", blank=True)

class TJLGAdvert(models.Model):
    weixin_link = models.CharField('推文连接',max_length=100)
    background_img = models.ImageField('背景图',upload_to='weixin_background_img',null=True, default="", blank=True)

    class Meta:
        verbose_name = '大个广告(天津理工)'
        verbose_name_plural = '大个广告(天津理工)'

class SchoolLife_TJLG(models.Model):
    author_name = models.CharField('作者名',max_length=20)
    avatar = models.ImageField('作者头像',upload_to='user_avatar',null=True, default="", blank=True)
    weixin_link = models.CharField('推文连接',max_length=100)
    background_img = models.ImageField('背景图',upload_to='weixin_background_img',null=True, default="", blank=True)

    class Meta:
        verbose_name = '校园生活(天津理工)'
        verbose_name_plural = '校园生活(天津理工)'