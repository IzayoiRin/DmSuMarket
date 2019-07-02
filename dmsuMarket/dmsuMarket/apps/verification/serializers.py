from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dmsuMarket.utils.serializers import RedisBaseSerializer
from verification import constants


class ImageCodeSerializer(RedisBaseSerializer):

    image_code_id = serializers.CharField(required=True)

    def create(self, validated_data):
        image_code_id = validated_data['image_code_id']
        text = getattr(self, 'text', None)
        assert text, 'ImageCodeSerializer saving to Redis losts a param <text>'
        self.redis.setex('img_%s' % image_code_id,
                         constants.IMAGE_CODE_REDIS_EXPIRES,
                         self.text)
        return {'image_code_id': image_code_id, 'text': text}


class SmsCodeSerializer(RedisBaseSerializer):

    image_code_id = serializers.CharField(required=True)
    text = serializers.CharField(required=True)

    class Meta:
        validate_rule = {'default': r'^[A-Za-z0-9]{4}$'}

    def validate(self, attrs):
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        try:
            validated_text = self.base_validate(text).upper()
        except ValidationError as e:
            self.redis.delete('img_%s' % image_code_id)
            raise ValidationError(e)
        else:
            redis_text = self.redis.get('img_%s' % image_code_id)
            redis_text = redis_text.decode('utf-8') if redis_text else None
            self.redis.delete('img_%s' % image_code_id)
            print('Verify:', image_code_id, validated_text, redis_text)
            if validated_text != redis_text:
                raise ValidationError("Image code is invalid")
            attrs['mobile'] = self.frequency_valid()
            return attrs

    def frequency_valid(self):
        context = getattr(self, 'context', None)
        mobile = context['view'].kwargs.get('mobile') if context else None
        assert mobile, 'Frequency validation losts a param <mobile>'
        flag = self.redis.get('flag_%s' % mobile)
        if flag:
            raise serializers.ValidationError("Request Frequently")
        return mobile

    def create(self, validated_data):
        mobile = validated_data['mobile']
        sms = getattr(self, 'sms', None)
        assert sms, 'SmsCodeSerializer saving to Redis losts a param <sms>'
        redis_pl = self.redis.pipeline()
        redis_pl.setex('mobile_%s' % mobile,
                       constants.SMS_CODE_REDIS_EXPIRES,
                       sms)
        redis_pl.setex('flag_%s' % mobile,
                       constants.FREQUENCY_FLAG_REDIS_EXPIRES,
                       1)
        redis_pl.execute()
        return {'mobile': mobile, 'sms': sms}
