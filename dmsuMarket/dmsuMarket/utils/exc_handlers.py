from rest_framework.views import exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status as s


logger = logging.getLogger('djlogger')


def g_exc_handler(exc, context):
    # exception handled by DRF exception_handler
    response = exception_handler(exc, context)
    # other exception caused by Database or RedisCache
    if response is None:
        view = context['view']
        if isinstance(exc, (DatabaseError, RedisError)):
            logger.error('@<{view}>{exc}'.format(view=view, exc=exc))
            response = Response({'msg': "SERVER INTERNAL ERROR"},
                                status=s.HTTP_507_INSUFFICIENT_STORAGE)
    return response
