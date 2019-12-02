from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# 方法二、通过新信号量创建用户 修改密码
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
        # 之后还需要进入app.py中设置
        """
        def ready(self):
            import users.signals
        """