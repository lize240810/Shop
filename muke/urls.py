"""muke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from muke.settings import MEDIA_ROOT, STATIC_ROOT
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls

admin.sites.AdminSite.site_header = 'QA管理系统'
admin.sites.AdminSite.site_title = '标题党'
admin.sites.AdminSite.index_title = '你想干嘛就干嘛'

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    path('api/', include('trade.urls')),
    path('api/', include('goods.urls')),
    path('api/', include('users.urls')),
    path('api/', include('user_operation.urls')),
    url(r'^docs/', include_docs_urls("文档"))
]

urlpatterns += [
    # url(r'^api-token-auth/', views.obtain_auth_token),  # drf 自带的token 认证
    url(r'^login/', obtain_jwt_token),  # jwt 所带的token认证接口
]
