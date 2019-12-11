from django.db.models import Q
from rest_framework import serializers

from .models import *


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


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


class GoodsSerializer(serializers.ModelSerializer):
    """商品：做序列化"""

    images = GoodsImageSerializer(many=True)
    category = CategorySerializer()

    def create(self, validated_data):
        """
        创建一个商品对象
        :param validated_data:
        :return:
        """
        return Goods.objects.create(**validated_data)

    class Meta:
        model = Goods
        fields = "__all__"


class HotGoodsSerializer(serializers.ModelSerializer):
    """
    热搜
    """

    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    """
    轮播图
    """

    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    """
    商品品牌
    """

    class Meta:
        model = GoodsCateGoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    """
        商品类别一对多
        这里为 GoodsCategory 是 GoodsCateGoryBrand 的主表，所以这里使用的话需要为many=True
        如果是在 BrandSerializer 中需要使用 GoodsCategorySerializer 的话 为副表引用主表 所以 many=False
    """
    # 反向序列化
    brands = BrandSerializer(many=True)
    # 自定义goods 的 serializer的方法
    goods = serializers.SerializerMethodField()
    # 数据需要二级类目
    sub_cat = CategorySerializer2(many=True)
    # 首页显示的商品信息
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        """
        显示首页商品类别的信息
        """
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            # 配置上 context={'request': self.context['request']} 在图片上才会拥有域名
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        """
        对goods 返回的数据进行操作
        """
        all_goods = Goods.objects.filter(
            Q(category_id=obj.id) |
            Q(category__parent_category_id=obj.id) |
            Q(category__parent_category__parent_category_id=obj.id)
        )
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
