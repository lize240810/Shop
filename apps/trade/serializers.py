import time
from random import Random

from rest_framework import serializers
from goods.serializers import GoodsSerializer
from .models import *

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
