from django.views.generic import View

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        # 通过django的view实现商品的列表
        json_list = []
        # 获取所有商品
        goods = Goods.objects.all()
        # for good in goods:
        #     json_dict = {}
        #     # 获取商品每个字段，以字典的形式
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        # return HttpResponse(json.dumps(json_list), content_type='application/json')

        # Django的serializer序列化
        import json
        from django.core import serializers
        from django.http import JsonResponse

        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)
