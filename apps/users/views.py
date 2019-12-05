from random import sample

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import *

User = get_user_model()


class CutomBackend(ModelBackend):
    """
    用户自定义验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 这里使用用户名和电话号码进行验证
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送验证码
    """
    queryset = VerifyCode.objects.all()
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成验证码code
        """
        seeds = '123456789'
        # 随机取验证码 并取六次
        return ''.join(sample(seeds, 6))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.is_valid(raise_exception=True)
            code1 = 0
            msg = '成功'
        except:
            code1 = 1,
            msg = '失败'

        # 获得手机号码
        mobile = serializer._validated_data['mobile']
        # 发送短信验证码的方法
        code = self.generate_code()
        print(code, mobile)
        sms_status = {
            'code': code1,
            'msg': msg
        }
        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 在发送之后保存， 防止短信发送失败
            verifycode = VerifyCode(mobile=mobile, code=code)
            verifycode.save()
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    用户注册
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        """
        动态修改serializer序列化
        """
        if self.action == 'create':
            return self.serializer_class
        else:
            return UserDetailSerializer

    def get_permissions(self):
        """
            动态设置权限
            - 用户注册时没有权限
            - 用户修改数据 或者用户查看自己数据时必须登录
        """
        # self.action 只有在使用viewset才有这个好处
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        # 使用注册并登录且返回token
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
        :return: 从结果集中返回一个用户
        """
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

