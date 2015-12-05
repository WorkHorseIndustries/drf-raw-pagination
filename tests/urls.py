from django.conf.urls import patterns, include, url
from rest_framework import routers

from test import views

router = routers.SimpleRouter

router.register('foo', views.FooView)
urlpatterns = routers.urls
