from django.contrib import admin
from .models import top_article_model
# Register your models here.

@admin .register(top_article_model)
class top_articleAdmin(admin.ModelAdmin):
    list_display = ('id','title','img','detail')
