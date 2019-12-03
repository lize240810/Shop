from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "后台管理"


# admin.site.site_title = '后台管理'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ['主要选项', {
            'fields': ('username',  'name', 'birthday', 'mobile', 'gender', 'email'),
        }],
        ['高级选项', {
            'classes': ('collapse',),  # CSS
            'fields': ('is_staff', 'is_active', 'is_superuser'),
        }]
    )
    # 自定义字段 只有再加入list_display中就可以使用了
    # def show_content(self, obj):
    #     return obj.content[:30]
    #
    # show_content.short_description = '评论内容'

    list_display = ["username", "mobile", "email", 'is_superuser']

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    list_filter = ('username', "mobile")

    # filter_horizontal = ('is_active', 'is_superuser')  # 给多选增加一个左右添加的框

    # 限制用户权限
    def get_queryset(self, request):
        qs = super(UserProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        self.fieldsets = (self.fieldsets[0], )
        return qs.filter(id=request.user.id)


@admin.register(VerifyCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "mobile", "add_time"]
