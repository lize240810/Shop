from rest_framework import serializers

from .models import *


class GoodsSerializer(serializers.ModelSerializer):
    """商品：做序列化"""

    def create(self, validated_data):
        """
        创建一个商品对象
        :param validated_data:
        :return:
        """
        return Goods.objects.create(**validated_data)

    class Meta:
        model = Goods
        fields = "__all__"  # ["name"]


class CategorySerializer3(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategoryPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategoryPrice
        fields = '__all__'
