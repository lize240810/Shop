import django_filters
from .models import Goods

from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.filterset.FilterSet):
    """
    商品的过滤类
    """
    pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte', help_text='最低价格')
    pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lte', help_text='最高价格')
    # 模糊查询
    # like_name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    top_category = django_filters.NumberFilter(method="top_category_filter", help_text='顶级类别', label='顶级类别')

    @staticmethod
    def top_category_filter(queryset, name, value):
        return queryset.filter(
            Q(category_id=value) |
            Q(category__parent_category_id=value) |
            Q(category__parent_category__parent_category_id=value)
        )

    class Meta:
        model = Goods
        fields = ["pricemin", "pricemax", 'top_category', 'is_new', 'is_hot']
