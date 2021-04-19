from django.test import TestCase
from Cred_Task_Api.models import counter,collection

# Create your tests here.
class CounterTest(TestCase):
    test_counter_name="Counter"

    def counter_test(self):
        result=counter.objects.get(counter_name=self.test_counter_name)
        result=result.number_of_request
        self.assertTrue(type(result) is str)

class Counterreset(TestCase):
    test_counter_name="Counter"

    def counter_reset(self):
        result=counter.objects.get(counter_name=self.test_counter_name)
        result.number_of_request=0
        result.save()
        self.assertEqual(result.number_of_request == 0)

class create_collection(TestCase):
    
    data={
        "title":"Collection_test",
        "description":"This is just for the testing purpose"
    }

    def test(self):
        get_data=self.data

        collection_obj=collection.objects.create(title=get_data["title"],description=get_data["description"])

        self.assertIsInstance(collection_obj, object)

class update_collection(TestCase):

    data={
        "uuid":"123e4567-e89b-12d3-a456-426614174000"
        "title":"Collection_test",
        "description":"This is just for the testing purpose"
    }

    def update(self):

        get_data=self.data

        collection_obj=collection.objects.get(id=get_data["uuid"]])
        collection_obj.title=get_data["title"]
        collection_obj.description=get_data["description"]
        collection_obj.save()

        self.assertIsInstance(collection_obj, object)
    
    def patching(self):
        
        get_data=self.data

        collection_obj=collection.objects.get(id=get_data["uuid"]])
        collection_obj.title=get_data["title"]
        collection_obj.save()

        self.assertIsInstance(collection_obj, object)



    
