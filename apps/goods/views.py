from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination

from .filters import *
from .serializers import *


class GoodsPagination(PageNumberPagination):
    page_size = 12
    # max_page_size = 80
    page_size_query_param = 'page_size'
    page_query_param = 'page'


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
    search_fields = ('name',)
    ordering_fields = ('sold_num', 'shop_price')

    def get_queryset(self):
        # print(self.request.META)
        print(self.request.user)
        return self.queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
    # lookup_field = ''

    # def get_queryset(self):
    #     if self.kwargs:
    #         return GoodsCategory.objects.filter(id=self.kwargs['pk'])
    #     return self.queryset


class GoodsCategoryPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsCategoryPrice.objects.all()
    serializer_class = GoodsCategoryPriceSerializer


class HotGoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotGoodsSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryVieweSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """

    # 在前端主页显示的商品类别目录 设置了 is_tab的才显示出来
    queryset = GoodsCategory.objects.filter(is_tab=True, category_type=1)  # name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer
