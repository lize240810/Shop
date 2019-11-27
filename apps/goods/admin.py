from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

admin.site.register(GoodsCateGoryBrand)

admin.site.register(GoodsImage)
admin.site.register(Banner)


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    """
    商品分页
    """
    # 列表页展示数据
    list_display = ["id", "name", "code", "category_type", "add_time", "is_tab"]
    # 过滤器
    list_filter = ['category_type']
    # 搜索
    search_fields = ['name']


@admin.register(Goods)
class GoodsAdmin(ImportExportModelAdmin):
    # exclude = ('name',)
    # 列表页展示数据
    list_display = ["category", "goods_sn", "name", "click_num", "sold_num", "fav_num", "goods_num", "shop_price",
                    "add_time", "is_new", "is_hot"]
    # 过滤器
    list_filter = ['add_time', 'category']
    # 搜索
    search_fields = ['name']
    # 内联
    # inlines = [TagInline]

    # fieldsets = (
    #     ['Main', {
    #         'fields': ('name', 'add_time'),
    #     }],
    #     ['Advanced options', {
    #         'classes': ('collapse',),  # CSS
    #         'fields': ('click_num', 'sold_num', 'goods_num'),
    #     }]
    # )
    raw_id_fields = ("category",)

    save_on_top = True


@admin.register(GoodsCategoryPrice)
class GoodsCategoryPriceAdmin(admin.ModelAdmin):
    list_display = ["category", "min_price", "max_price"]

    # 设置外键筛选
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = GoodsCategory.objects.filter(category_type=1)
        return super.formfield_for_foreignkey(db_field, request, **kwargs)
