import json

from django.conf import settings
from django.utils import timezone

from twilio.rest import TwilioRestClient
import twilio.twiml

from .models import Contact, Message

from rest_framework import renderers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route


from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from .serializers import ContactSerializer, MessageSerializer

from .tasks import *

class MessagingViewSet(viewsets.ViewSet):

    @list_route(methods=['post'])
    def catch(self, request, format='xml'):
        '''
        Deals with the incoming payload,
        Creates a new message object connected to the Contact
        '''
        message = str(request.data['Body'])
        to_number = request.data['From']

        contact = Contact.objects.filter(phone_number=to_number).first()

        if not contact:
            print "Unknown contact messaging you"
            contact = Contact.objects.create(
                first_name='Unknown',
                last_name='',
                phone_number=to_number
                )

        new_message = Message.objects.create(
            text=message,
            contact=contact,
            )

        message_serialized = serialize(MessageSerializer(new_message))

        redis_publisher = RedisPublisher(facility='akalite', broadcast=True)
        web_message = RedisMessage(message_serialized)
        redis_publisher.publish_message(web_message)
      
        print('Message successfuly caught.')

        resp = twilio.twiml.Response()
        resp.message("Caught")

        return Response(None)

    @list_route(methods=['get'])
    def get_contacts(self, request):
        '''
        This function will print/retrieve all of the contact objects
        '''
        contacts_query = Contact.objects.all()
        contacts = ContactSerializer(contacts_query, many=True).data

        return Response(contacts)

    @list_route(methods=['get'])
    def get_messages(self, request):
        '''
        Returns messages attributed to a contact
        '''
        contact_id = request.GET['contact_id']

        ordered_messages = Contact.objects.get(id=contact_id).messages.all()
        messages = MessageSerializer(ordered_messages, many=True).data

        return Response(messages)

    @list_route(methods=['post'])
    def add_contact(self, request):
        ''' 
        This function deals with the addition of a new contact to 
        the contact list
        '''
        incoming_data = request.data
        data = json.loads(request.body)

        print data

        first_name = data.get('contact.firstName')
        last_name = data.get('contact.lastName')
        phone_number = data.get('contact.phoneNumber')

        phone_number = clean_number(phone_number)

        new_contact = Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
            )


    @list_route(methods=['post'])
    def send_message(self,request):
        twilio_client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
       
        message = str(json.loads(request.data['params']['message'])['message_field'])
        contact_id = json.loads(request.data['params']['contact'])['id']
        number = str(json.loads(request.data['params']['contact'])['phone_number'])


        if number and contact_id and message:
            twilio_client.sms.messages.create(
                body=message,
                to=number,
                from_=settings.MY_TWILIO_NUMBER
            )
            print number
            
            contact = Contact.objects.get(id=contact_id)     
            new_message = Message.objects.create(
                text=message,
                contact=contact,
                sent_by_me=True,
                )

            _message = MessageSerializer(new_message).data

        return Response(_message)