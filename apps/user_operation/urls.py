from django.conf.urls import url, include


from rest_framework.routers import DefaultRouter

from .views import *
router = DefaultRouter()

# 配置goods的url
router.register(r'userfavs', UserFavViewSets)

urlpatterns = [
    url(r'^', include(router.urls)),
]

