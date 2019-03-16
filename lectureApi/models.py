from django.db import models

# Create your models here.
class Lecture(models.Model):
    start_time_list = (
        (1,"第一节课"),
        (2, "第二节课"),
        (3, "第三节课"),
        (4, "第四节课"),
        (5, "第五节课"),
        (6, "第六节课"),
        (7, "第七节课"),
        (8, "第八节课"),
        (9, "第九节课"),
    )
    length_list = {
        (1, "二节课"),
        (2,"二节课"),
        (3, "三节课"),
        (4, "四节课"),
    }
    headline = models.CharField("活动名",max_length=30)
    title = models.CharField("题目（选填）",max_length=30,null=True,blank=True)
    speaker = models.CharField("主讲人",max_length=30)
    host = models.CharField("主持人（选填）",max_length=30,null=True,blank=True)
    time = models.DateTimeField("时间(日期格式必须为2019/03/17，时间格式必须为13:32)",auto_now_add=False)
    start_time = models.IntegerField("开始时间",choices=start_time_list)
    length = models.IntegerField("持续时长",choices=length_list)
    location = models.CharField("地点",max_length=50)
    intro = models.CharField("主讲人简介(最多120字)",max_length=120,default="暂无主讲人简介")
    class Meta:
        verbose_name = '课表自定义显示内容'
        verbose_name_plural = '课表自定义显示内容'