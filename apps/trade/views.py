from rest_framework import views
from rest_framework import viewsets, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from utils.permissions import IsOwnerOrReadOnly
from utils.alipay import *
from muke.settings import PRIVATE_KEY_PATH, ALIPAY_KEY_PATH


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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderInfoSerializer

    def get_queryset(self):
        """
        设置只能查询到当前用户自己的购物车
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        保存订单编号的时候
        从购物车中遍历数据出来，然后把商品与商品数量赋值给订单
        然后删除购物车中的商品，保存到订单中
        """
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order


from rest_framework.response import Response


class AliPayView(views.APIView):
    """
    支付宝请求回调视图
    return_url: 同步通知 url 支付完成之后，支付宝将传入的return_url 通过get请求
    app_notify_url: 异步通知 url 通过post方式请求
    """

    def get(self, request):
        """
        处理支付宝的url返回
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            # 沙箱里面的appid值
            appid="2016092600599306",
            # notify_url是异步的url 比 reuturn_url 还重要
            app_notify_url="http://47.98.34.221:8888/api/alipay/return",  #
            # 我们自己商户的密钥
            app_private_key_path=PRIVATE_KEY_PATH,
            # 支付宝的公钥
            alipay_public_key_path=ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,
            return_url="http://47.98.34.221:8888/api/alipay/return"  # 支付成功之后导向地址
        )

        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            # 订单编号
            order_sn = processed_dict.get('order_sn', None)
            # 支付编号
            trade_no = processed_dict.get('trade_no', None)
            # 支付状态
            trade_status = processed_dict.get('trade_status', None)

            # 根据顶单编号查询对应的订单
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)

            for existed_order in existed_orders:
                # 修改订单数据
                existed_order.order_sn = order_sn
                existed_order.trade_no = trade_no
                existed_order.pay_status = trade_status
                existed_order.pay_time = datetime.now()
                existed_order.save()

        return Response("success")

    def post(selfs, request):
        """
        处理notify_url
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            # 沙箱里面的appid值
            appid="2016092600599306",
            # notify_url是异步的url 比 reuturn_url 还重要
            app_notify_url="http://47.98.34.221:8888/api/alipay/return",  #
            # 我们自己商户的密钥
            app_private_key_path=PRIVATE_KEY_PATH,
            # 支付宝的公钥
            alipay_public_key_path=ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,
            return_url="http://47.98.34.221:8888/api/alipay/return"  # 支付成功之后导向地址
        )

        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            # 订单编号
            order_sn = processed_dict.get('order_sn', None)
            # 支付编号
            trade_no = processed_dict.get('trade_no', None)
            # 支付状态
            trade_status = processed_dict.get('trade_status', None)

            # 根据顶单编号查询对应的订单
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)

            for existed_order in existed_orders:
                # 修改订单数据
                existed_order.order_sn = order_sn
                existed_order.trade_no = trade_no
                existed_order.pay_status = trade_status
                existed_order.pay_time = datetime.now()
                existed_order.save()

        return Response("success")
