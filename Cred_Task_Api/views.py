from rest_framework import status
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import environ
from retrying import retry
import requests
import base64
import json
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from Cred_Task_Api.models import collection,movies,counter
from Cred_Task_Api.serializers import collection_serializers,movie_serializers
from rest_framework.renderers import JSONRenderer
from django.db import models, transaction, OperationalError
from rest_framework.decorators import api_view, renderer_classes


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


env = environ.Env()
environ.Env.read_env()

class get_movies_from_thirdparty_api(APIView):
    permission_classes = [AllowAny]

    username=env('username_api')
    password=env('password_api')
    auth_string=f"{username}:{password}"
    
    def format_auth(self):
        return b'Basic '+base64.b64encode(self.auth_string.encode())

    @retry(stop_max_attempt_number=7,wait_fixed=2000)
    def safe_request(self,url, **kwargs):
        get_collections=requests.get(url,headers={'Authorization':self.format_auth()})
        get_collections=json.dumps(get_collections.json())
        return get_collections

    def get(self,request):
        return Response(self.safe_request(env('thirdparty_url')))

class register_user(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        user=get_user_model()
        username=request.data["username"]
        password=request.data["password"]
        is_created=user(username=username,email="dummy@gmail.com")
        is_created.set_password(password)
        is_created.save()
        user_created=user.objects.get(username=username)
        payload = jwt_payload_handler(user_created)
        token = jwt_encode_handler(payload)
        return Response(json.dumps({"access_token":token}))

class login_user(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        user=get_user_model()
        username=request.data["username"]
        password=request.data["password"]
        is_authenticated=authenticate(username=username,password=password)
        if is_authenticated:
            payload = jwt_payload_handler(is_authenticated)
            token = jwt_encode_handler(payload)
            return Response(json.dumps({"access_token":token}))
        else:
            return Response(json.dumps({"0":"Bad Credential"}))

class register_collection(APIView):
    
    permission_classes = [AllowAny]

    renderer_classes = [JSONRenderer]


    def post(self,request):

        payload_received=request.data

        collection_title=payload_received["title"]
        collection_description=payload_received["description"]
        

        register_collections=collection.objects.create(title=collection_title,description=collection_description)

        collection_pkey=collection.objects.get(id=register_collections.pk)

        for each_movie in payload_received["movies"]:
            movie_title=each_movie["title"]
            movie_description=each_movie["description"]
            movie_genres=each_movie["genres"]
            movie_uuid=each_movie["uuid"]
            
            movie_register=movies.objects.create(title=movie_title,description=movie_description,genres=movie_genres,movie_uuid=movie_uuid,collection_id=collection_pkey)

        return Response({"collection_uuid":register_collections.pk})
    
    def get(self,request):

        from collections import Counter

        get_all_genres=[]

        get_queryset=collection.objects.all()

        for each_movies in movies.objects.all():
            if each_movies.genres:
                get_all_genres+=each_movies.genres.split(",")
        
        get_fav_genres=Counter(get_all_genres).most_common(3)

        serialized_response=collection_serializers(get_queryset,many=True)

        serialized_response_formatting= {
            "is_success":True,
            "data":{
                "collections":serialized_response.data
            },
            "favourite_genres":get_fav_genres
        }

        return Response(serialized_response_formatting)

class modify_collection(APIView):

    renderers=[JSONRenderer]

    permission_classes = [AllowAny]

    def no_object_found(self,collection_uuid):
        return Response({
            "Bad Request":f"No Object {collection_uuid} Found"
        },status=status.HTTP_404_NOT_FOUND)

    def put(self,request,collection_uuid):

        payload_received=request.data

        collection_title=payload_received["title"]

        collection_description=payload_received["description"]
        try:

            get_collection_object=collection.objects.get(id=collection_uuid)

        except ObjectDoesNotExist as err:

            return self.no_object_found(collection_uuid)

        get_collection_object.title=collection_title

        get_collection_object.description=collection_description
        
        get_collection_object.save()

        return Response({"Collection_uuid Updated Successfully":collection_uuid})

    def get(self,request,collection_uuid):
        try:

            get_collection_object=collection.objects.get(id=collection_uuid)

        except ObjectDoesNotExist as err:

            return self.no_object_found(collection_uuid)

        serialized_response=collection_serializers(get_collection_object)

        get_all_movies_collectionwise=get_collection_object.movie_list.all()

        serialized_response_movies=movie_serializers(get_all_movies_collectionwise,many=True)

        formatted_data={
            "Collection":serialized_response.data,
            "movies":serialized_response_movies.data
        }

        return Response(formatted_data)

    def delete(self,request,collection_uuid):
        try:

            get_collection_object=collection.objects.get(id=collection_uuid)
        
        except ObjectDoesNotExist as err:

            return self.no_object_found(collection_uuid)
        
        get_collection_object.delete()
        
        return Response({"Successfully Deleted":collection_uuid})

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_request_count(request):
    if request.method=="GET":
        get_counter=counter.objects.get(counter_name="Counter")
        return Response({
            "Number of request served": str(get_counter.number_of_request)
        })
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def reset_request_count(request):
    if request.method=="GET":
        with transaction.atomic():
            get_counter=counter.objects.filter(counter_name="Counter").update(number_of_request=0)
        return Response({
            "Message": "Request Count Reset Successfully"
        })
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)






