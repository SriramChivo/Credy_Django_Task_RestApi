from django.contrib import admin
from django.urls import path,include
from Cred_Task_Api.views import (get_movies_from_thirdparty_api,register_user,login_user,
                                register_collection,modify_collection,get_request_count,reset_request_count)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('movies/',get_movies_from_thirdparty_api.as_view(),name="get_movies"),
    path('register/',register_user.as_view(),name="register_user"),
    path('login/',login_user.as_view(),name="login_user"),
    path('collection/',register_collection.as_view(),name="register_collection"),
    path('collection/<uuid:collection_uuid>/',modify_collection.as_view(),name="modify_collection"),
    path('api-token-auth/', obtain_jwt_token),
    path('request-count/',get_request_count,name="get_req_count"),
    path('request-count/reset/',reset_request_count,name="reset_request_count"),
]
