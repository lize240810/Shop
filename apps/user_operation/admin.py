from django.contrib import admin

# Register your models here.
from .models import *

# 把模型注册到admin中
admin.site.register(UserFav)
admin.site.register(UserLeavingMessage)
admin.site.register(UserAddress)
