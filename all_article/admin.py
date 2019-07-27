from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_time', 'last_updated_time')

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('title','create_time')

@admin.register(ahuUser)
class ahuUserAdmin(admin.ModelAdmin):
    list_display = ('id','Sno','userAvatar')

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('id','author', 'excerpt','like_num','created_time','img')

@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'like_num','create_time', 'user','article')


@admin.register(UserActionLike)
class UserActionLikeAdmin(admin.ModelAdmin):
    list_display = ('id','user','action')



@admin.register(UserCommentLike)
class UserCommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id','user','comment')