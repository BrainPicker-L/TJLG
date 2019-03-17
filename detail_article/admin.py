from django.contrib import admin
from .models import DetailArticle
# Register your models here.
@admin.register(DetailArticle)
class DetailArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'last_updated_time')