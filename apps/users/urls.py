from django.conf.urls import url, include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
# 配置goods的url
router.register(r'code', SmsCodeViewset)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]


