#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : jwt登陆验证
# __REFERENCES__ : https://www.jianshu.com/p/dec4fe44255b
# __date__: 2020/09/28 14

from .utils import get_username_field, get_user_model, get_payload, get_user, get_username, jwt_payload_handler, jwt_encode_handler
from datetime import datetime
from django.contrib.auth import get_user_model, authenticate

from django.core.exceptions import ValidationError
from datetime import datetime
from .settings import api_settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
User = get_user_model()
# fetch handlers from settings
jwt_response_from_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def jwt_base_handler(user, token):
    response_data = jwt_response_payload_handler(token, user)
    if api_settings.JWT_AUTH_COOKIE:
        expiration = (datetime.utcnow() +
                      api_settings.JWT_EXPIRATION_DELTA)
        return response_data, expiration
    else:
        return response_data


def jwt_token_verify_handler(token):
    payload = get_payload(token=token)
    user = get_user(payload=payload)
    res = jwt_base_handler(user, token)
    return res


def jwt_token_refresh_handler(token):
    payload = get_payload(token=token)
    user = get_user(payload=payload)
    return {
        'token': token,
        'user': get_username(user)
    }


def jwt_login_handler(username, password):
    username_field = get_username_field()
    credentials = {username_field: username, 'password': password}
    if credentials:
        user = authenticate(**credentials)
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise ValidationError(msg)

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)
    else:
        msg = _('Must include "{username_field}" and "password".')
        msg = msg.format(username_field=username_field)
        raise ValidationError(msg)
    res = jwt_base_handler(user, token)
    return res

