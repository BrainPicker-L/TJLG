from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(ahuUser)
class ahuUserAdmin(admin.ModelAdmin):
    list_display = ('id','Sno','wx_name','userAvatar','unread_num')

@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('id','type','author', 'excerpt','position','like_num','created_time','img')

@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'like_num','create_time', 'user','article')

@admin.register(UserActionLike)
class UserActionLikeAdmin(admin.ModelAdmin):
    list_display = ('id','user','action')



@admin.register(UserCommentLike)
class UserCommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id','user','comment')


@admin.register(allNotice)
class allNoticeAdmin(admin.ModelAdmin):
    list_display = ('id','movement','movementer','noticeer','action','create_time')

@admin.register(stickieAction)
class stickieActionAdmin(admin.ModelAdmin):
    list_display = ('id','action_id')