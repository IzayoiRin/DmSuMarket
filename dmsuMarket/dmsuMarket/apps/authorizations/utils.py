import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


def jwt_response_payload_handler(token, instance, request):
    return {
        'token': token,
        'user_id': instance.id,
        'username': instance.username
    }


def get_authenticate_field(raw_field):
    """
    Multi-type Authentication with different fields whose config is
    setting.AUTHENTICATION_FIELDS = {'UserModelAuthenticatingFields':'RegExp'}
    Authentication is ordered by this config, holding up by field, username
    :param raw_field:
    :return:
    """
    fields = settings.AUTHENTICATION_FIELDS
    for field, rule in fields.items():
        if re.match(rule, raw_field):
            return field


class UsersModelBackends(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = self.field_distinction(username)
        return super().authenticate(request, username, password, **kwargs)

    @staticmethod
    def field_distinction(raw_field):
        UserModel = get_user_model()
        field = get_authenticate_field(raw_field)
        if hasattr(UserModel, field) if field else None:
            UserModel.USERNAME_FIELD = field
        return UserModel
