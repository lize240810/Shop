# -*- coding: utf-8 -*-
__author__ = 'bobby'
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))  # 获得当前 运行的目录
sys.path.append(pwd + "../")  # 把根目录添加到环境变量中
# 最关键的一部， 从manage.py文件中复制出来 指定django环境变量
# 想要单独使用django.model 必须设置的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muke.settings')

# 为了直接使用django
import django

django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage
from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

    category_name = goods_detail["categorys"][-1]

    # 根据 商品类型 查询
    # 这里使用filter 而不使用get 是为了 不引发异常 get会引发异常
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        # 添加外键
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()
