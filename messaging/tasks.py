from rest_framework.renderers import JSONRenderer
from .models import *
def clean_number(number):
    if number[0] != '1':
        number = '+1' + number
    if number[0] != '+':
        number = '+' + number

    return number

def serialize(serialized):
	return JSONRenderer().render(serialized.data)

def delete_all_messages():
	'''
	Deletes all messages associated with one contact
	'''
	messages = Message.objects.all()
	messages.delete()
