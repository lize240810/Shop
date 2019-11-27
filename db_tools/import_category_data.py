# -*- coding: utf-8 -*-
__author__ = 'bobby'

# 独立使用django的model
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

from goods.models import GoodsCategory
from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    # print(lev1_cat['sub_categorys'])
    lev1_intance = GoodsCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()
    # print(lev1_intance)

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()
        # print('\t', lev2_intance)
        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()
            # print('\t\t', lev3_intance)
