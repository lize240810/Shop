from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

from .serializers import *
from .filters import *


class GoodsPagination(PageNumberPagination):
    page_size = 12
    # max_page_size = 80
    page_size_query_param = 'page_size'
    page_query_param = 'page'


# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表页
#     """
#     # 数据集
#     queryset = Goods.objects.all()
#     # 序列化
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination

class GoodsListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    商品列表页
    """
    # 数据集
    queryset = Goods.objects.all()

    # 序列化
    serializer_class = GoodsSerializer
    # 分页
    pagination_class = GoodsPagination
    # 过滤
    # token 认证
    # authentication_classes = (TokenAuthentication, )

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('shop_price',)  # 相等过滤
    filter_class = GoodsFilter
    search_fields = ('name', )
    ordering_fields = ('sold_num', 'shop_price')

    def get_queryset(self):
        # print(self.request.META)
        print(self.request.user)
        return self.queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class GoodsCategoryPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsCategoryPrice.objects.all()
    serializer_class = GoodsCategoryPriceSerializer
