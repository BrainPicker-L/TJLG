from django.contrib import admin
from .models import Article,Email
# Register your models here.
@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_time', 'last_updated_time')
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('title','create_time')