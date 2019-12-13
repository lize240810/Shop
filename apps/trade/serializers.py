import time
from random import Random

from rest_framework import serializers
from goods.serializers import GoodsSerializer
from .models import *
from apps.utils.alipay import *
from muke import settings

random = Random()


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    nums = serializers.IntegerField(default=1, label='购买数量', min_value=1, error_messages={
        'min_value': '商品数量不能小于一'
    })
    # 商品必须是已经存在的商品 还可以加filter 进行其他的限制
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all())

    def create(self, validated_data):
        """
        重写创建验证方法
        """
        # 用户
        user = self.context['request'].user
        # 商品
        nums = validated_data['nums']
        goods = validated_data['goods']
        # 判断当前用户的该商品是否添加过
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        # 判断存在则修改数量后保存
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    class Meta:
        model = ShoppingCart
        fields = ('user', 'nums', 'goods')


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = ShoppingCart
        fields = ('nums', 'goods')


class OrderGoodsSerializer(serializers.ModelSerializer):
    # 外键关系 所以使用False
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    OrderGoods 中使用了两个外键关联
    这里就让OrderGoods与商品信息进行外键相关联 goods = GoodsSerializer(many=False)
    再进行反序列化 goods = OrderGoodsSerializer(many=True)
    """
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    # goods = GoodsSerializer()

    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_time = serializers.CharField(read_only=True)
    # 只能读不能写
    order_sn = serializers.CharField(read_only=True)

    pay_status = serializers.CharField(read_only=True)

    trade_no = serializers.CharField(read_only=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        """
         与支付宝交付返回支付url
        :param obj: serializer对象
        """
        # 测试用例
        alipay = AliPay(
            # 沙箱里面的appid值
            appid="2016092600599306",
            # notify_url是异步的url 比 reuturn_url 还重要
            app_notify_url="http://47.98.34.221:8888/api/alipay/return",  #
            # 我们自己商户的密钥
            app_private_key_path=settings.PRIVATE_KEY_PATH,
            # 支付宝的公钥
            alipay_public_key_path=settings.ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.98.34.221:8888/api/alipay/return"  # 支付成功之后导向地址
        )
        # 直接支付:生成请求的字符串。
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.order_mount
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        """
        生成订单编号
        :return:
        """
        order_sn = "{timestr}{userid}{randomstr}".format(
            timestr=time.strftime('%Y%m%d%H%M%S'),
            userid=self.context['request'].user.id,
            randomstr=random.randint(10, 99)  # 区间值
        )
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        attrs['trade_no'] = random.randint(100, 999)
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'
