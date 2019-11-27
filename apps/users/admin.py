from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = "后台管理"
# admin.site.site_title = '后台管理'
admin.site.register(UserProfile)
admin.site.register(VerifyCode)

