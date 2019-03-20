from django.contrib import admin
from .models import Menu
@admin.register(Menu)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('diningRoom','winNum','namePrice')
