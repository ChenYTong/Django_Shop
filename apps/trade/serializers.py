from random import Random

import time
from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods


class ShopCartDetailSerializer(serializers.ModelSerializer):
    # 设置动态serializer
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShopCartSerializer(serializers.Serializer):
    """
    序列化商品列表
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={
                                        'min_value': '商品数量不能小于1',
                                        'required': '选择购买数量'
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all(), label='商品名称')

    # 重写create的方法
    def create(self, validated_data):
        """
        加入购物车有两种情况
        1 购物车没有此商品新建
        2 购物车里面有次商品,直接增加
        """
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        # 查询数据库,查看商品是否存在
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        # 如果购物车里已经存在次商品
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        # 如果购物车没有存在次商品
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        # 最后返回购物车的状态
        return existed

    # 在继承serializer,create,update,delete诸多方法需要重写
    # 当继承ModelSerializer时，则不需要重写
    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 系统设置默认订单状态为待支付
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    pay_type = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        """
        订单号：当前时间+userid+随机数
        """
        random_ins = Random()
        order_sn = '{time_str}{userid}{ranstr}'.format(time_str=time.strftime('%Y%m%d%H%M%S'),
                                                       userid=self.context['request'].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


# 订单中的商品
class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


# 订单商品信息
# goods字段需要嵌套一个OrderGoodsSerializer
class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerialzier(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"
