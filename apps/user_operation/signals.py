from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserFav


# 信号量 修改用户收藏
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        # 收藏数+1
        goods = instance.goods
        goods.fav_num += 1
        goods.save()
        # 之后还需要进入app.py中设置
        """
        def ready(self):
            import users.signals
        """


@receiver(post_delete, sender=UserFav)
def destory_userfav(sender, instance=None, created=False, **kwargs):
    """
    用户取消收藏
    商品收藏数就减一
    """
    # 收藏数+1
    goods = instance.goods
    if goods.fav_num > 0:
        goods.fav_num -= 1
        goods.save()
