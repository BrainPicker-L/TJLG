from django.contrib import admin
from .models import Lecture
# Register your models here.
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('headline', 'title', 'speaker', 'host','time','start_time','length','location','intro')
