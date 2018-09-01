from rest_framework import serializers
from goods.models import Goods, GoodsCategory, GoodsImage


# ModelSerializer实现商品列表页
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image', )


# # ModelSerializer实现实现商品列表页
class GoodsSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'
