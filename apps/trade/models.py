from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model  # django user的模型

from goods.models import Goods

User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    nums = models.IntegerField(default=0, verbose_name="购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
        订单中的商品是一对多的关系,所以需要多个商品
    """
    ORDER_STATUS = (
        ('success', "成功"),
        ("cancel", "取消"),
        ("cancel", "待支付")
    )
    PAY_TYPE = (
        ("alipay", "支付宝"),
        ("wechat", "微信")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    order_sn = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="订单唯一编号")
    # 第三方支付成功返回一个编号 我们与本地关系
    trade_no = models.CharField(max_length=100, unique=True, verbose_name="第三方支付订单编号")
    pay_status = models.CharField(max_length=30, verbose_name="支付状态")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    post_script = models.CharField(max_length=200, verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="支付金额")

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name="地址")
    sing_name = models.CharField(max_length=30, default="", verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, verbose_name="签收人电话")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


class OrderGoods(models.Model):
    """订单商品详情"""
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单编号")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    goods_num = models.IntegerField(default=0, verbose_name="订单数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_sn
