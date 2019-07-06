from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^users/$', UsersAPI.as_view(), name='create_user')
]
