from django.db import models
from datetime import datetime

class Contact(models.Model):
	first_name=models.CharField(max_length=20, blank=True,null=True)
	last_name=models.CharField(max_length=20,blank=True, null=True)
	phone_number=models.CharField(max_length=15,blank=True, null=True)

	def __str__(self):
		return self.first_name


class Message(models.Model):
	text=models.TextField()
	time_stamp = models.DateField(auto_now_add=True, auto_now=False, blank=True, null=True)
	sent_by_me = models.BooleanField(default=False)
	contact=models.ForeignKey(
		Contact, 
		blank=True,
		null=True,
		related_name='messages'
		)
	def __str__(self):
		return self.text