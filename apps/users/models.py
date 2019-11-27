from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户,这里是继承的底层User模型 我们这里只是新增一些字段
    """
    # null=True, blank=True 允许为空
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='用户名')
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")  # 年龄保存出生日期
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")),
                              default="female", verbose_name="性别")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="电子邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name if self.name else self.username)


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    # datetime.now() 的话有问题
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

