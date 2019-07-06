import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings

from dmsuMarket.utils.serializers import RedisBaseSerializer
from users.models import UserModel


class UserSerializer(RedisBaseSerializer, serializers.ModelSerializer):

    password2 = serializers.CharField(required=True ,write_only=True)
    sms_code = serializers.CharField(required=True, write_only=True)
    allow = serializers.CharField(required=True, write_only=True)

    class Meta:

        model = UserModel
        fields = ('id', 'password', 'username', 'mobile',
                  'password2', 'sms_code', 'allow')
        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 5,
                'error_messages': {
                    'max_length': 'must between 5 and 20',
                    'min_length': 'must between 5 and 20',
                }
            },
            'password': {
                'write_only': True,
                'max_length': 20,
                'min_length': 8,
                'error_messages': {
                    'max_length': 'must between 8 and 20',
                    'min_length': 'must between 8 and 20',
                }
            }
        }

    def validate_mobile(self, value):
        if re.match(r'^1[3-9]/d{9}$', value):
            raise ValidationError('Illegal Phone Number')
        return value

    def validate_allow(self, value):
        if value == 'true':
            return value
        raise ValidationError('Plz agree with the protocol')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError('Confirm your password again')
        redis_sms = self.redis.get('mobile_%s' % attrs['mobile'])
        if attrs['sms_code'] != (redis_sms.decode('utf-8') if redis_sms else None):
            raise ValidationError('Invalidated Sms Code')
        self.redis.delete('mobile_%s' % attrs['mobile'])
        del attrs['sms_code']
        del attrs['allow']
        del attrs['password2']
        return attrs

    def create(self, validated_data):
        user = super().create(validated_data)  # type: UserModel
        user.set_password(validated_data['password'])
        user.save()
        return user

    def save(self, **kwargs):
        super().save(**kwargs)
        self.jwt_signer()

    def jwt_signer(self):
        payload_h = api_settings.JWT_PAYLOAD_HANDLER
        encode_h = api_settings.JWT_ENCODE_HANDLER
        token = encode_h(payload_h(self.instance))
        self.instance.token = token
