from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ("username","avatar","email","is_staff","is_active","is_superuser")

    def avatar(self, obj):
        return obj.profile.avatar
    avatar.short_description = "用户头像"
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','avatar')