from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^image-codes/(?P<image_code_id>[\w-]+)/$', ImageCodeAPI.as_view())
]