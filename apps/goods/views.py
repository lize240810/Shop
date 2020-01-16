from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination  # 分页
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin  # 缓存
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle  # 限速 防爬虫

from .filters import *
from .serializers import *


class GoodsPagination(PageNumberPagination):
    """
    分页
    """
    page_size = 12
    # max_page_size = 80
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class GoodsListViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
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
    # 过滤类型
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('shop_price',)  # 相等过滤
    filter_class = GoodsFilter
    search_fields = ('name',)  # 查询
    ordering_fields = ('sold_num', 'shop_price')  # 排序
    # 限速设置
    throttle_classes = (AnonRateThrottle, UserRateThrottle)

    def get_queryset(self):
        # print(self.request.META)
        print(self.request.user)
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        # 修改点击数
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


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
