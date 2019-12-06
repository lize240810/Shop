from .serializers import *
from rest_framework import viewsets, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartSets(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'

    def get_queryset(self):
        """
        设置只能查询到当前用户自己的购物车
        """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['get', 'list', 'retrieve']:
            return ShoppingCartDetailSerializer
        return self.serializer_class


class OrderSets(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    订单视图 不允许修改
    """
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        """
        设置只能查询到当前用户自己的购物车
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        return order