from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import authentication
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from My_Shop.settings import APIKEY
from users.models import VerifyCode
from users.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

User = get_user_model()


class CustomBackend(ModelBackend):
    """ 自定义用户验证规则 """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            #  后期可以添加邮箱验证
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            #  UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成4位随机验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        sms_status = yun_pian.send_sms(code=self.generate_code(), mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=self.generate_code(), mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 权限设置方法一
    # permission_classes = (permissions.IsAuthenticated, )
    # 权限设置方法二

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def crate(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data

        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
