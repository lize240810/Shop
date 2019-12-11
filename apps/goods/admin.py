from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *


@admin.register(GoodsCateGoryBrand)
class GoodsCateGoryBrandAdmin(admin.ModelAdmin):
    list_display = ["category", "name", "add_time"]
    fk_fields = ('category',)

    # raw_id_fields = ("category",)

    # 设置外键筛选
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = GoodsCategory.objects.filter(category_type=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(GoodsImage)
admin.site.register(Banner)


# 文档教程 https://www.cnblogs.com/wumingxiaoyao/p/6928297.html
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
    list_display = ["name", "category", "goods_sn", "click_num", "sold_num", "fav_num", "goods_num", "shop_price",
                    "add_time", "is_new", "is_hot"]
    # 过滤器
    list_filter = ['add_time', 'category']
    # 搜索
    search_fields = ['name']

    list_display_links = ['name']
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
    # 可以修改的
    # list_editable = ['is_new']

    # fk_fields = ('category',)

    save_on_top = True

    # def get_readonly_fields(self, request, obj=None):
    #     """  重新定义此函数，限制普通用户所能修改的字段  """
    #     if request.user.is_superuser:
    #         self.readonly_fields = []
    #     return self.readonly_fields
    #
    # readonly_fields = ('machine_ip', 'status', 'user', 'machine_model', 'cache',
    #                    'cpu', 'hard_disk', 'machine_os', 'idc', 'machine_group')


@admin.register(GoodsCategoryPrice)
class GoodsCategoryPriceAdmin(admin.ModelAdmin):
    list_display = ["category", "min_price", "max_price"]

    # 设置外键筛选
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = GoodsCategory.objects.filter(category_type=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(HotSearchWords)


@admin.register(IndexAd)
class IndexAdAdmin(admin.ModelAdmin):
    list_display = ['category', 'goods']

    # 设置外键筛选
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.attname == 'category_id':
            kwargs["queryset"] = GoodsCategory.objects.filter(category_type=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
