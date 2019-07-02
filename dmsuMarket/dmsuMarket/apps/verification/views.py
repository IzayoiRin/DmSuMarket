from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from dmsuMarket.utils.captcha.captcha import captcha
from dmsuMarket.utils.renderers import JPEGRenderer
from verification.serializers import ImageCodeSerializer


class ImageCodeAPI(GenericAPIView):

    serializer_class = ImageCodeSerializer
    renderer_classes = (JPEGRenderer,)

    # /image_codes/(?P<image_code_id>[\w-]+)/
    def get(self, request, image_code_id):
        _, text, img = captcha.generate_captcha()
        print(text)
        s = self.get_serializer(data={'sid': image_code_id})
        setattr(s, 'text', text)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(data=img, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        s = super().get_serializer(*args, **kwargs)    # type: SessionSerializer
        s.validate_rule = r'^.*'
        s.redis = 'imgcode'
        return s


class SmsCodeAPI(GenericAPIView):

    serializer_class = ''

