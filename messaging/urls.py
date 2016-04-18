from django.conf.urls import url, include

from . import views
from .viewsets import MessagingViewSet

from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'chat', MessagingViewSet, '')


urlpatterns = [
    url(r'^$', views.homeView.as_view(), name='homeView'),
    url(r'^messaging/$', views.messagingView.as_view(), name='messagingView'),
]

urlpatterns += router.urls
