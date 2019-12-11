from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

# 配置goods的url
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', CategoryViewSet)
router.register(r'category_price', GoodsCategoryPriceViewSet)
router.register(r'banners', BannerViewSet)
router.register(r'hotsearchs', HotGoodsViewSet)
router.register(r'indexgoods', IndexCategoryVieweSet)


urlpatterns = [
    url(r'^', include(router.urls))
]


