from import_export import resources
from .models import *


class GoodsResource(resources.ModelResource):
    class Meta:
        model = Goods
