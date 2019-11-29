import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from .models import *
from muke.settings import REGULAR_MOBILE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11)

    def validate_mobile(self, mobile):
        # 使用正则 验证手机号码
        if not re.match(REGULAR_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不符合")

        # 验证发送频率
        # 一分钟以前
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 验证码添加时间大于一分钟以前的时间
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60S")

        # 判断手机号码是否注册过
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机号码已被注册")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    # 自己添加的字段
    # required 必填
    # help_text 提示消息
    #
    code = serializers.CharField(
        max_length=6, min_length=6, required=True,
        help_text="验证码",
        error_messages={
            'blank': '请输入验证码',
            'required': "请输入验证码",
            'max_length': "验证码格式错误",
            'min_length': "验证码格式错误"
        }
    )

    username = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        # 判断是否唯一
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已存在")],
        error_messages={
            'blank': '请输入用户名',
            'required': "请输入用户名"
        }
    )
    mobile = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    # 验证码出错的可能
    def validate_code(self, code):
        """
            验证码验证错误的原因
            1. 不存在 用户输入错误的
            2. serializers 的验证
            3. 过期
        """
        # 验证码是否存在 或者过期
        # 手机号码里的验证记录
        # ModelSerializer中前端传过来的值 都在 self.initial_data 中
        # 查询该号码最后一次验证的时间
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by("-add_time")
        if verify_codes:
            last_record = verify_codes.first()

            # 获得前五分钟
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 判断最近的一次发送记录是否在五分钟之内 否在就验证码过期
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            # 判断验证码是否正确
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        """
        字段统一的处理
        :param attrs:
        :return:
        """
        attrs['mobile'] = attrs['username']
        attrs.pop('code')
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile')
