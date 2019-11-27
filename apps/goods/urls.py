from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', CategoryViewSet)
router.register(r'category_price', GoodsCategoryPriceViewSet)

urlpatterns = [
    # path(r'goods/', GoodsListView.as_view())
    # path(r'goods/', goods_list)
    url(r'^', include(router.urls))
]


