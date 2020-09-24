#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/09/08 09

import os
import datetime
import json

from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .handler import get_ml_1m_zip,hello_word_handler
from apps.utils.wsme.signature import signature
from .types import HelloWordResult, HelloWordBody

class hello_word_view(generic.View):
    """ hello_word_view """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(hello_word_view, self).dispatch(*args, **kwargs)

    # @signature(HelloWordResult, body=HelloWordBody)
    # def post(self, request, *args, **kwargs):
    #     content = hello_word_handler()
    #     res = HelloWordResult(content=content)
    #     return res
    @signature(HelloWordResult)
    def get(self):
        content = get_ml_1m_zip()
        return HelloWordResult(content=content)

