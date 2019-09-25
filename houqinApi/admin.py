from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Gongdan)
class WorksAdmin(admin.ModelAdmin):
    list_display = ('gongdanid','status','repair_man','name','phonenum','pos','abletime','excerpt','created_time')

@admin.register(RepairMan)
class RepairManAdmin(admin.ModelAdmin):
    list_display = ('id','name','phonenum')


@admin.register(StatusName)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','name')

