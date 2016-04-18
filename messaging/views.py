from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class homeView(TemplateView):
	template_name="messaging/homepage.html"

class messagingView(TemplateView):
	template_name="messaging/messaging.html"