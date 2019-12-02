from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "后台管理"


# admin.site.site_title = '后台管理'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ['主要选项', {
            'fields': ('username', 'birthday', 'mobile', 'gender', 'email'),
        }],
        ['高级选项', {
            'classes': ('collapse',),  # CSS
            'fields': ('is_staff', 'is_active', 'is_superuser'),
        }],
        # ['权限分配', {
        #     'classes': ('collapse',),  # CSS
        #     'fields': ('is_staff', 'is_active', 'is_superuser'),
        # }]
    )
    list_display = ["username", "mobile", "email", 'is_superuser']


@admin.register(VerifyCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "mobile", "add_time"]
