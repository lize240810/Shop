from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# 配置goods的url
router.register(r'shopcarts', ShoppingCartSets)
router.register(r'orders', OrderSets)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'alipay/return', AliPayView.as_view(), name='alipay'),
]
