from django.db import models

# Create your models here.
class ahuUser(models.Model):
    Sno = models.CharField("学号", max_length=12)
    userAvatar = models.ImageField("学生微信头像", upload_to='user_avatar', null=True, default="", blank=True)
    unread_num = models.IntegerField("未阅读消息数", default=0)
    wx_name = models.CharField("微信名称", max_length=100, null=True, default="", blank=True)

    class Meta:
        verbose_name = '用户信息（动态）'
        verbose_name_plural = '用户信息（动态）'

    def __str__(self):
        return "<学生学号：%s>" % self.Sno


class ActionType(models.Model):
    name = models.CharField('动态种类名称',max_length=50)
    def __str__(self):
            return "<动态种类：%s>" % self.name

class UserAction(models.Model):
    author = models.ForeignKey(ahuUser, on_delete=models.CASCADE)
    type = models.ForeignKey(ActionType, on_delete=models.CASCADE,blank=True,null=True)
    excerpt = models.CharField("动态内容", max_length=300)
    position = models.CharField("地点",max_length=300,default="",null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    like_num = models.IntegerField("点赞数", default=0)
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
    class Meta:
        verbose_name = '动态点赞表'
        verbose_name_plural = '动态点赞表'

class UserCommentLike(models.Model):
    user = models.ForeignKey(ahuUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='like_comments',
                                verbose_name='喜欢的评论')
    class Meta:
        verbose_name = '评论点赞表'
        verbose_name_plural = '评论点赞表'

class allNotice(models.Model):
    movement = models.CharField('动作名称',max_length=20)
    noticeer = models.ForeignKey(ahuUser,on_delete=models.CASCADE,verbose_name='动作通知的人',related_name='noticeer', null=True, blank=True)
    movementer = models.ForeignKey(ahuUser,on_delete=models.CASCADE,verbose_name='动作发起者',related_name='movementer')
    action = models.ForeignKey(UserAction, on_delete=models.CASCADE, verbose_name='动作目标文章')
    create_time = models.DateTimeField('动作起始时间', auto_now_add=True)
    class Meta:
        verbose_name = '动态通知表'
        verbose_name_plural = '动态通知表'

class stickieAction(models.Model):
    action_id = models.IntegerField('文章id',default=0)

