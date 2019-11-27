from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别
    通过一个Model 完成多级类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别编码", help_text="类别编码")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类别种类", help_text="类别种类")
    # 这里进行多级类别 自己指向自己的, 为空的话 就证明是一级目录
    # related_name="sub_cat"用于查询的时候
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类别", on_delete=models.CASCADE
                                        , related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否是导航", help_text="是否是导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryPrice(models.Model):
    """
    类别价格
    """
    min_price = models.IntegerField(verbose_name="最小价格", help_text="最小价格")
    max_price = models.IntegerField(verbose_name="最大价格", help_text="最大价格")
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类别")

    class Meta:
        verbose_name = "商品类别价格"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}(max:{1}, min{2})".format(self.category.name, self.max_price, self.min_price)


class GoodsCateGoryBrand(models.Model):
    """
    商品品牌
    """
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, verbose_name="商品类别", on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(default="", verbose_name="简单描述", help_text="简单描述")
    # upload_to=  指定图片上传时候 保存路径
    image = models.ImageField(max_length=200, upload_to="brands/", verbose_name="Logo")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类别", on_delete=models.CASCADE)
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一编码")  # 售货员拿货
    name = models.CharField(max_length=300, verbose_name="商品名称")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="卖出量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存量")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(verbose_name="商品短暂描述")
    goods_desc = UEditorField(verbose_name="内容", imagePath="goods/images/", width=1000, height=200,
                              filePath='goods/files/', default="")  # 富文本
    ship_free = models.BooleanField(default=True, verbose_name="是否免运费")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图片")
    is_new = models.BooleanField(default=False, verbose_name="是否是新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热卖商品")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='goods/images/', verbose_name="图片", null=True, blank=True)
    # image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name="图片URL")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)  # related_name="images"
    image = models.ImageField(upload_to='branner/', verbose_name="轮播图图片", null=True, blank=True)
    index = models.IntegerField(default=0, verbose_name="轮播图顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
