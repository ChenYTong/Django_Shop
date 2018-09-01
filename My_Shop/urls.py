"""My_Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from My_Shop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewset
from user_operation.views import UserFavViewset
from users.views import SmsCodeViewset, UserViewset

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name='goods')

router.register(r'categorys', CategoryViewset, base_name='categorys')

router.register(r'codes', SmsCodeViewset, base_name='codes')

router.register(r'users', UserViewset, base_name='users')

router.register(r'userfavs', UserFavViewset, base_name='userfavs')

goods_list = GoodsListViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='陈氏集团')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),
]
