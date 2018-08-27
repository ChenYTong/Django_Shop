from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins

from goods.filters import GoodsFilter
from goods.models import Goods, GoodsCategory

from goods.serializers import CategorySerializer, GoodsSerializer
from rest_framework import filters


# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods = Goods.objects.all()
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)

# 第一种分页
# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# 实现分页方法2
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_siz'
    page_query_param = 'page'
    max_page_size = 100


# class GoddsListView(generics.ListAPIView):
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # 商品列表页
    queryset = Goods.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'shop_price')
    # 搜索 name表示精确搜索
    # filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # # 排序
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
