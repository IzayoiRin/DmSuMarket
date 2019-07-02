from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^image-codes/(?P<image_code_id>[\w-]+)/$', ImageCodeAPI.as_view()),
    url(r'^sms-codes/(?P<mobile>1[3-9]\d{9})/$', SmsCodeAPI.as_view()),
]
