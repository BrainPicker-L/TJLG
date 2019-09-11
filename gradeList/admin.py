from django.contrib import admin
from .models import *

@admin.register(student_Id)
class student_IdAdmin(admin.ModelAdmin):
    list_display = ('xuehao','created_time')


@admin.register(gradeInfo)
class gradeInfoAdmin(admin.ModelAdmin):
    list_display = ('grade_id','unique_key','subject','property','grade')


@admin.register(Guake)
class GuakeAdmin(admin.ModelAdmin):
    list_display = ('id','Name')

@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ('id','kcmc','ls','extra')