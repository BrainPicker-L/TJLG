from django.db import models



# class RepairMan(models.Model):
#     name = models.CharField("维修工姓名",max_length=50)
#     phonenum = models.CharField("维修工电话号码", null=True,blank=True,max_length=100)
#     class Meta:
#         verbose_name = '维修人员'
#         verbose_name_plural = '维修人员'
#     def __str__(self):
#         return "<维修工：%s>" % self.name

class StatusName(models.Model):
    name = models.CharField("维修状态名",max_length=50)
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
    def __str__(self):
        return "<当前维修状态：%s>" % self.name

class Gongdan(models.Model):
    gongdanid = models.CharField("工单号",max_length=50,null=True,blank=True)
    sno = models.CharField("学号",max_length=50)
    name = models.CharField("姓名",max_length=50)

    excerpt = models.TextField("故障描述",null=True, blank=True)
    reply = models.TextField("后勤回复",null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    status = models.ForeignKey(StatusName, null=True, blank=True, on_delete=models.CASCADE, default=None)
    phone_num = models.CharField("手机号", max_length=50,default='')
    class Meta:
        verbose_name = '工单'
        verbose_name_plural = '工单'
    def __str__(self):
        return "<工单号：%s>" % self.pk