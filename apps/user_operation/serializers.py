from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    # 获取登当前陆的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        # validate实现唯一连个，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                # message信息可以自定义
                message='已收藏'
            )
        ]
        # 收藏的时候需要返回商品的id,因为取消收藏的时候必须知道商品的id
        fields = ('user', 'goods', 'id')
