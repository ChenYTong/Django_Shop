from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from user_operation.models import UserFav
from user_operation.serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    用户收藏
    mixins.CreateModelMixin 添加收藏（相当于创建数据库）
    mixins.DestroyModelMixin 取消删除（相当于数据库删除）
    mixins.ListModelMixin 获取已收藏的商品列表
    """
    # permission是用来做权限判断的
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # auth使用来做用户认证的
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 搜索的字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只能查看当前登录用户的收藏，不会获取所有用户的收藏
        return UserFav.objects.filter(user=self.request.user)
"""
只有登录用户才可以收藏
用户只能获取自己的收藏，不能获取所有用户的收藏
JSONWebTokenAuthentication认证不应该全局配置，
因为用户获取商品信息或者其它页面的时候并不需要此认证，所以这个认证只要局部中添加就可以
删除settings中的'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
"""