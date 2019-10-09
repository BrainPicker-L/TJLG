from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Gongdan)
class WorksAdmin(admin.ModelAdmin):
    list_display = ('gongdanid','status','name','excerpt','reply','created_time')



@admin.register(StatusName)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','name')

