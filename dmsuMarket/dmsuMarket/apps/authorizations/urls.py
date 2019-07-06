from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # POST /authorizations/
    # username password return json{username, user_id, token}
    url(r'^authorizations/$', obtain_jwt_token)
]
