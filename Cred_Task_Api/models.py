from django.db import models
import uuid

# Create your models here.

class collection(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=125,blank=False)
    description=models.CharField(max_length=500,blank=False)

    def __str__(self):
        return self.title[:25]
    
    class Meta:

        verbose_name_plural="Collection"

class movies(models.Model):
    
    title=models.CharField(max_length=125,blank=False)
    description=models.CharField(max_length=500,blank=False)
    genres=models.CharField(max_length=100,blank=False)
    movie_uuid=models.UUIDField(default=uuid.uuid4)
    collection_id=models.ForeignKey(collection,on_delete=models.CASCADE,related_name="movie_list")

    def __str__(self):
        return self.title[:25]
    
    class Meta:

        verbose_name_plural="Movie"

class counter(models.Model):
    counter_name=models.CharField(max_length=10,default="Counter")
    number_of_request=models.IntegerField(default=0)
    
    def __str__(self):
        return str(number_of_request)


