import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *
from goods.serializers import GoodsSerializer
from muke.settings import REGULAR_MOBILE


class UserFavSerializer(serializers.ModelSerializer):
    # 使用内置方法获得当前用户并覆盖现在的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

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


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("id", 'goods')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # read_only=True 只返回不提交
    # 控制时间格式
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'msg_type', 'subject', 'message', 'file', 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def validate_signer_mobile(self, signer_mobile):
        # 使用正则 验证手机号码
        if not re.match(REGULAR_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码不符合")
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'district', 'address', 'signer_name', 'signer_mobile', 'province', 'city', 'add_time')


