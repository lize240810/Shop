from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    删除的时候验证一个权限问题
    自定义的一个权限方法，用于判断请求用户是否和数据库中的当前用户相同
    """

    def has_object_permission(self, request, view, obj):
        """
        检查obj
        :param request:
        :param view:
        :param obj: 就是从数据库中取出来的obj
        :return:
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        # 判断数据库中取出来的user与请求的user是否是同一个
        return obj.user == request.user
