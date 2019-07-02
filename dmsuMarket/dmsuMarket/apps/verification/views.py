import random

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from dmsuMarket.utils.captcha.captcha import captcha
from dmsuMarket.utils.renderers import JPEGRenderer
from verification.serializers import ImageCodeSerializer, SmsCodeSerializer


class ImageCodeMixin(object):

    # GET /image-codes/(?P<image_code_id>[\w-]+)/
    def image_(self, request, image_code_id):
        _, text, img = captcha.generate_captcha()
        s = self.get_serializer(data={'image_code_id': image_code_id})
        s.is_valid(raise_exception=True)
        setattr(s, 'text', text)
        ret = s.save()
        print(">>>>> UUID:{image_code_id} >>>>>> ImgCode: {text} >>>>>".format(**ret))
        return Response(data=img, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        s = super().get_serializer(*args, **kwargs)    # type: ImageCodeSerializer
        s.validate_rule = r'^.*'
        s.redis = self.redis_con
        return s


class SmsCodeMixin(object):
    # GET /sms-codes/(?P<mobile>1[3-9]\d{9})/?image_code_id=&text=
    def sms_(self, request, mobile):
        s = self.get_serializer(data=request.query_params)
        s.is_valid(raise_exception=True)
        sms = '%06d' % random.randint(0, 999999)
        print('>>>>>>>>>>>>Clouds Communicating>>>>>>>>>>>>>>')
        setattr(s, 'sms', sms)
        ret = s.save()
        print(">>>>> Mobile:{mobile} >>>>>> SmsCode: {sms} >>>>>".format(**ret))
        return Response(data={'message': 'OK'}, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        s = super().get_serializer(*args, **kwargs)  # type: SmsCodeSerializer
        s.redis = self.redis_con
        return s


class ImageCodeAPI(ImageCodeMixin, GenericAPIView):
    """
    GET /image-codes/(?P<image_code_id>)/
    Request:
        :path_param: image_code_id UUIDField
    Serializer: ImageCodeSerializer
    Renderer: JPEGRenderer
        :return
            JPG  BinaryType
    """

    serializer_class = ImageCodeSerializer
    redis_con = 'verification'
    renderer_classes = (JPEGRenderer,)

    def get(self, request, *args, **kwargs):
        return self.image_(request, *args, **kwargs)


class SmsCodeAPI(SmsCodeMixin, GenericAPIView):
    """
    GET /sms-codes/(?P<mobile>1[3-9]\d{9})/?image_code_id=UUID&text=XXXX
    Request:
        :path_param: mobile
        :query_params: QueryDict{image_code_id: UUIDField, text: r'^[A-Za-z0-9]{4}$'}
    Serializer: SmsCodeSerializer
    Renderer: JOSNRenderer
        :return
            {'message': ok}
            {'non_field_errors': error}
    """

    serializer_class = SmsCodeSerializer
    redis_con = 'verification'
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return self.sms_(request, *args, **kwargs)
