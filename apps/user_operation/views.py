from rest_framework import mixins, viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSets(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    list:
        获取收藏列表
    delete:
        取消收藏
    create:
        添加收藏
    retrieve:
        判断某个商品是否收藏
    """
    queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # permission_classes = (IsAuthenticated, )
    serializer_class = UserFavSerializer
    # 进入该视图必须带上jwt token认证
    # session 认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # jwt token 验证
    # 设置搜索字段, 这里是在get_queryset 之后的数据中进行操作
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        """
        过滤用户
        """
        return UserFav.objects.filter(user=self.request.user)


class LeavingMessageSets(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = UserLeavingMessage.objects.all()
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # jwt token 验证

    def get_queryset(self):
        """
        过滤用户
        """
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressSets(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # jwt token 验证
    serializer_class = AddressSerializer

    def get_queryset(self):
        """
        过滤用户
        """
        return UserAddress.objects.filter(user=self.request.user)
