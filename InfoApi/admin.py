from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(StartSchoolDay)
class StartSchoolDayAdmin(admin.ModelAdmin):
    list_display = ('id','time')