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





class ahuUser(models.Model):
    Sno = models.CharField("学号",max_length=12)
    userAvatar = models.ImageField("学生微信头像",upload_to='user_avatar',null=True, default="", blank=True)
    class Meta:
        verbose_name = '用户信息（动态）'
        verbose_name_plural = '用户信息（动态）'
    def __str__(self):
        return "<学生学号：%s>" % self.Sno

class UserAction(models.Model):
    author = models.ForeignKey(ahuUser, on_delete=models.CASCADE)
    excerpt = models.CharField("动态内容",max_length=300)
    created_time = models.DateTimeField(auto_now_add=True)
    like_num = models.IntegerField("点赞数",default=0)
    img = models.ImageField("图片1", upload_to='action_img', null=True, default="", blank=True)
    class Meta:
        verbose_name = '已发内容（动态）'
        verbose_name_plural = '已发内容（动态）'
    def __str__(self):
        return "<文章主键：%s>" % self.pk


class BaseComment(models.Model):
    '基础评论模型'
    content = models.TextField('评论', max_length=500)
    create_time = models.DateTimeField('评论时间', auto_now_add=True)
    like_num = models.IntegerField("点赞数", default=0)
    user = models.ForeignKey(ahuUser, on_delete=models.CASCADE, verbose_name='评论者')
    class Meta:
        abstract = True


class ArticleComment(BaseComment):
    '文章评论'
    article = models.ForeignKey(UserAction, on_delete=models.CASCADE, related_name='comments', verbose_name='评论文章')
    class Meta:
        verbose_name = '评论（动态）'
        verbose_name_plural = '评论（动态）'
    def __str__(self):
        return "<评论主键：%s>" % self.pk

class UserActionLike(models.Model):
    user = models.ForeignKey(ahuUser, on_delete=models.CASCADE)
    action = models.ForeignKey(UserAction, on_delete=models.CASCADE, related_name='like_action', verbose_name='喜欢的文章')

class UserCommentLike(models.Model):
    user = models.ForeignKey(ahuUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='like_comments', verbose_name='喜欢的评论')

class SchoolLife(models.Model):
    author_name = models.CharField('作者名',max_length=20)
    avatar = models.ImageField('作者头像',upload_to='user_avatar',null=True, default="", blank=True)
    weixin_link = models.CharField('推文连接',max_length=100)
    background_img = models.ImageField('背景图',upload_to='weixin_background_img',null=True, default="", blank=True)

class AhuAdvert(models.Model):
    weixin_link = models.CharField('推文连接',max_length=100)
    background_img = models.ImageField('背景图',upload_to='weixin_background_img',null=True, default="", blank=True)

class SchoolLife_TJLG(models.Model):
    author_name = models.CharField('作者名',max_length=20)
    avatar = models.ImageField('作者头像',upload_to='user_avatar',null=True, default="", blank=True)
    weixin_link = models.CharField('推文连接',max_length=100)
    background_img = models.ImageField('背景图',upload_to='weixin_background_img',null=True, default="", blank=True)

    class Meta:
        verbose_name = '校园生活(天津理工)'
        verbose_name_plural = '校园生活(天津理工)'