from rest_framework import serializers
from goods.serializers import GoodsSerializer
from .models import *


class ShoppingCartSerializer(serializers.ModelSerializer):

    nums = serializers.IntegerField(default=1, label='购买数量', min_value=1, error_messages={
        'min_value': '商品数量不能小于一'
    })
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
        fields = ('nums', 'goods')

# class ShoppingCartDetailSerializer(serializers.ModelSerializer):
#     add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
#
#     goods = GoodsSerializer()
#
#     class Meta:
#         model = ShoppingCart
#         fields = '__all__'
