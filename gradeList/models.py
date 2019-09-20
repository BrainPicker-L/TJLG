from django.db import models

class student_Id(models.Model):
    xuehao = models.CharField("学号",max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)



class gradeInfo(models.Model):
    grade_id = models.CharField("课程号",max_length=30)
    unique_key = models.CharField("学号+课程号",max_length=50,default="")
    subject = models.CharField("课程名称",max_length=30)
    property = models.CharField("课程性质",max_length=30)
    grade = models.CharField("分数",max_length=30)



class Guake(models.Model):
    Code = models.CharField(verbose_name="课程号",max_length=50)
    Name = models.CharField(verbose_name='课程名',max_length=50)
    Number = models.CharField(verbose_name="人基数",max_length=50)
    Category = models.CharField(verbose_name='课程类型',max_length=50)
    P0_59 = models.CharField(verbose_name="0-59",max_length=50)
    P60_69 = models.CharField(verbose_name="60-69", max_length=50)
    P70_79 = models.CharField(verbose_name="70-79", max_length=50)
    P80_89 = models.CharField(verbose_name="80-89", max_length=50)
    P90_100 = models.CharField(verbose_name="90-100", max_length=50)

class ClassInfo(models.Model):
    kcmc = models.CharField(verbose_name='课程名称',max_length=50)
    ls = models.CharField(verbose_name='老师',max_length=50)
    kcdd = models.CharField(verbose_name='课程地点',max_length=50)
    xqj = models.IntegerField("星期几", default=0)
    skjc = models.IntegerField("上课开始", default=0)
    skcd = models.IntegerField("上课长度", default=0)
    qszs = models.IntegerField("起始周数", default=0)
    jszs = models.IntegerField("结束周数", default=0)
    dsz = models.IntegerField("单双周", default=0)
    extra = models.TextField("課程信息")