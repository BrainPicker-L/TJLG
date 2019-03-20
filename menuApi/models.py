from django.db import models

# Create your models here.
class Menu(models.Model):
    diningRoom = models.CharField("食堂",max_length=20)
    winNum = models.CharField("窗口",max_length=20)
    namePrice = models.CharField("菜品名称/价格",max_length=100)
    class Meta:
        verbose_name = '食堂菜单内容'
        verbose_name_plural = '食堂菜单内容'