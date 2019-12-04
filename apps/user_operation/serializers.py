from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator


class UserFavSerializer(serializers.ModelSerializer):
    # 使用内置方法获得当前用户并覆盖现在的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # goods = GoodsSerializer(many=True)

    class Meta:
        model = UserFav
        # 唯一方法二
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "goods"),
                message="已经收藏"
            )
        ]
        fields = ("user", "id", 'goods')
