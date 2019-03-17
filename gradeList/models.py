from django.db import models

class student_Id(models.Model):
    xuehao = models.CharField("学号",max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)



class gradeInfo(models.Model):
    grade_id = models.CharField("课程号",max_length=30)
    subject = models.CharField("课程名称",max_length=30)
    property = models.CharField("课程性质",max_length=30)
    grade = models.CharField("分数",max_length=30)