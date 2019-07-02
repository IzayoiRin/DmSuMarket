from rest_framework import serializers

from dmsuMarket.utils.serializers import RedisBaseSerializer
from verification import constants


class ImageCodeSerializer(RedisBaseSerializer):

    sid = serializers.CharField(required=True)

    def create(self, validated_data):
        image_code_id = validated_data['sid']
        return self.redis.setex('img_%s' % image_code_id,
                                constants.IMAGE_CODE_REDIS_EXPIRES,
                                self.text)
