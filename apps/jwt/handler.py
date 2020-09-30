#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : jwt登陆验证
# __REFERENCES__ : https://www.jianshu.com/p/dec4fe44255b
# __date__: 2020/09/28 14

from .serializers import VerifyJSONWebTokenSerializer, RefreshJSONWebTokenSerializer, JSONWebTokenSerializer
from .compat import get_username_field
import json
from datetime import datetime

from django.contrib.auth import get_user_model

from datetime import datetime
from .settings import api_settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
User = get_user_model()
# fetch handlers from settings
jwt_response_from_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


def jwt_base_handler(user, token):
    response_data = jwt_response_payload_handler(token, user)
    if api_settings.JWT_AUTH_COOKIE:
        expiration = (datetime.utcnow() +
                      api_settings.JWT_EXPIRATION_DELTA)
        return response_data, expiration
    else:
        return response_data


def jwt_token_verify_handler(token):
    ser = VerifyJSONWebTokenSerializer(data={'token': token})
    ser.is_valid(raise_exception=True)
    user = ser.object.get('user')
    token = ser.object.get('token')
    res = jwt_base_handler(user, token)
    return res


def jwt_token_refresh_handler(token):
    ser = RefreshJSONWebTokenSerializer(data={'token': token})
    ser.is_valid(raise_exception=True)
    return jwt_response_from_payload_handler(**ser.initial_data)


def jwt_login_handler(username, password):
    ser = JSONWebTokenSerializer(
        data={get_username_field(): username, 'password': password})
    ser.is_valid(raise_exception=True)
    user = ser.object.get('user')
    token = ser.object.get('token')
    res = jwt_base_handler(user, token)
    return res
