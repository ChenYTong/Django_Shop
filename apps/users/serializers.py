import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from My_Shop.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, help_text='手机号码')

    def validate_mobile(self, mobile):
        # 手机是否注册
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError('用户已经存在')

        # 手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码格式不正确')

        # 验证码发送频率
        # 60秒只能发送一次
        one_mintes_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_age, mobile=mobile).count():
            raise serializers.ValidationError('距离上次发送信息未超过60s')

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'gender', 'birthday', 'email', 'mobile')


class UserRegSerializer(serializers.Serializer):

    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, help_text='验证码')
    username = serializers.CharField(label='用户名', required=True, allow_blank=False, help_text='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # mobile = models.CharField(null=True, blank=True, max_length=11)
    password = serializers.CharField(style={'input_type': 'password'}, label='密码', write_only=True, help_text='密码')
    # 不使用这个 使用信号量, 把数据库的密码转变成密文
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # 用户注册,已post方式提交信息,数据保存在initial_data里
        # username是用户注册的手机号码,验证码按照添加的时间排序
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

        if verify_records:
            # 最近的一个验证码
            last_record = verify_records[0]
            # 有效期为5分钟
            five_minutes_age = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)

            if five_minutes_age > last_record.add_time:
                raise serializers.ValidationError('验证码过期')

            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

        # 所有字段,atter是字段验证合法之后返回的总dict
        def validate(self, attrs):
            # 前段没有传mobile到后端,这里添加
            attrs['mobile'] = attrs['username']
            # code 是自己添加,数据库在没有这个字段,验证完成后删除
            del attrs['code']
            return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
