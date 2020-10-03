#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 
# __REFERENCES__ : 
# __date__: 2020/10/03 13
from rest_framework import serializers

import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import ugettext as _
from apps.api_exception import ParameterException


class ApisResult(wtypes.Base):
    status_code = wsme.wsattr(int, default=200)
    content = _types.jsontype
    detail = wsme.wsattr(wtypes.text, default=str(_('success')))


class TestSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=20, required=True)
    status_code = serializers.CharField(max_length=20, required=True)
