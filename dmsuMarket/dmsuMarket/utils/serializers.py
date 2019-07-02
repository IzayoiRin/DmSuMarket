import logging
import re

from django_redis import get_redis_connection
from redis import RedisError
from rest_framework import serializers

logger = logging.getLogger('djlogger')


class RedisBaseSerializer(serializers.Serializer):

    __validate_rule = None

    class Meta:

        redis_base = None
        validate_rule = {'default': r'^[A-Z0-9a-z-]+$'}

    @property
    def redis(self):
        if self.Meta.redis_base is None:
            logging.warning('Connecting Redis First')
        return self.Meta.redis_base

    @redis.setter
    def redis(self, basename):
        try:
            self.Meta.redis_base = get_redis_connection('imgcode')
        except Exception as e:
            raise RedisError('Redis connecting Failed: %s' % e)

    @property
    def validate_rule(self):
            return self.__validate_rule or self.Meta.validate_rule['default']

    @validate_rule.setter
    def validate_rule(self, rule: str):
        if isinstance(rule, str):
            if rule.startswith('^'):
                self.__validate_rule = rule
                return
            logging.warning('Rule should be regular expression start with "^"')
            self.__validate_rule = rule
        logging.error('Rule should be regular expression')

    def base_validate(self, value):
        if re.match(self.validate_rule, value):
            return value
        raise serializers.ValidationError("{value} not allowed by {rule}"
                                          .format(value=value, rule=self.validate_rule))
