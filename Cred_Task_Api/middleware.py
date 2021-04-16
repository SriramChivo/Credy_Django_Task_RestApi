from django.utils.deprecation import MiddlewareMixin
from Cred_Task_Api.models import counter
from django.db import models, transaction, OperationalError


class CounterMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            get_counter=counter.objects.get(counter_name="Counter")
            with transaction.atomic():
                get_counter.number_of_request=get_counter.number_of_request+1
                get_counter.save()
        except:
            get_counter=counter.objects.create(counter_name="Counter",number_of_request=1)
        
        #this is will show each user how many request has been served
        hit = request.session.get('hit')
        if not hit:
            request.session['hit'] = 1
        else: 
            request.session['hit'] += 1
        print(request.session['hit'])
        return None