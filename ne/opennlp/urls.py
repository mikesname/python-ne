"""XLS Import URLs."""

from django.conf.urls.defaults import *

from . import forms, views


urlpatterns = patterns('',
    url(r'^$', views.home, name="home"),
)


