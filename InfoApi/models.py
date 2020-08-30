from django.db import models

# Create your models here.
class StartSchoolDay(models.Model):
    time = models.DateTimeField('开学时间', auto_now_add=False)