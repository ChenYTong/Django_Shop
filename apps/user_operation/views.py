from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
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

    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer
    # auth使用来做用户认证的
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 搜索的字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只能查看当前登录用户的收藏，不会获取所有用户的收藏
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin,
                            mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list 获取用户留言
    create 添加留言
    delete 删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址
    list 获取收货地址
    create 添加收货地址
    update 更新收货地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
