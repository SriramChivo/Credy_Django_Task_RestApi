from rest_framework import serializers
from Cred_Task_Api.models import collection,movies


class collection_serializers(serializers.ModelSerializer):

    class Meta:

        model = collection
        fields="__all__"

class movie_serializers(serializers.ModelSerializer):

    class Meta:

        model = movies
        fields=['title','description','genres','movie_uuid']