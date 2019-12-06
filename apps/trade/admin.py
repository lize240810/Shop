from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['goods', 'user', 'add_time']
    list_filter = ('user',)


admin.site.register(OrderInfo)
admin.site.register(OrderGoods)
