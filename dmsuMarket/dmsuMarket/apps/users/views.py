from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer

from users.serializers import UserSerializer


class UsersAPI(CreateAPIView):
    """
    POST /users/
    username password password2 sms_code mobile allow
    return Json{id, username, mobile}
    """
    serializer_class = UserSerializer
    redis_conn = 'verification'
    renderer_classes = (JSONRenderer,)

    def get_serializer(self, *args, **kwargs):
        s = super().get_serializer(*args, **kwargs)  # type: UserSerializer
        s.redis = self.redis_conn
        return s
