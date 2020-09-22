#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 12:40:21

import os
import datetime
import json

from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.utils.wsme.signature import signature
from .types import HelloWordResult, HelloWordBody,ComputeAprioriBody
from .models.apriori import apriori,loadDataSet

@signature(HelloWordResult, body=ComputeAprioriBody)
def compute_apriori_view(body):
    params = {
        'data':body.data, 
        'minSupport':body.minSupport, 
        'max_k':body.max_k
        }
    content = apriori(params)
    res = HelloWordResult(content=content)
    return res