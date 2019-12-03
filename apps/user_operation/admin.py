from django.contrib import admin

# Register your models here.
from .models import *

# 把模型注册到admin中
@admin.register(UserFav)
class UserFavAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods', 'add_time']


admin.site.register(UserLeavingMessage)
admin.site.register(UserAddress)
