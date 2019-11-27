import re
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import *
from muke.settings import REGULAR_MOBILE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        # 使用正则 验证手机号码
        if not re.match(REGULAR_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不符合")

        # 验证发送频率
        # 一分钟以前
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=60, seconds=0)
        # 验证码添加时间大于一分钟以前的时间
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60S")

        # 判断手机号码是否注册过
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机号码已被注册")

        return mobile