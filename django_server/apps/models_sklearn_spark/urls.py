#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/09/08 09

from django.conf.urls import url
from .views import hello_word_view
app_name = 'models'
urlpatterns = [
    url(r'^hello_word/$', hello_word_view.as_view(), name='hello_word'),
]
