#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 基于https://github.com/SimpleJWT/django-rest-framework-simplejwt 开发jwt-TOKEN验证脚手架
# __REFERENCES__ :
# __date__: 2020/10/10 14
from apps.utils.wsme import json
import inspect
import logging
import re
from datetime import date
import six
from apps.api_exception import InvalidJwtToken, InvalidUser
from apps.apis.serializers import UserSerializer
from apps.role.models import get_role_via_user

from apps.utils.core.session.handler import session_logout, _get_user_session_key, session_user_update
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenObtainSlidingSerializer,
    TokenRefreshSerializer, TokenRefreshSlidingSerializer)

from .models import UserInfoSerializer, token_get_user_model
from django.contrib.auth import get_user_model

log = logging.getLogger('apps')


def token_obtain_sliding_logout_handler(**params):
    """
    用户登出，更新用户信息，注销request信息等
    """
    try:
        current_request = params.get('request')
        assert params.get('request')
        session_logout(current_request)
    except Exception as e:
        log.warn(e)
        raise InvalidJwtToken(msg=six.text_type(e))
    return '登出成功'


def token_obtain_sliding_login_handler(request, username, password):
    """
    Takes a set of user credentials and returns a sliding JSON web token to
    prove the authentication of those credentials.
    """
    ser = TokenObtainSlidingSerializer(
        data={get_username_field(): username, 'password': password})
    try:
        ser.is_valid(raise_exception=True)
    except:
        raise InvalidUser('用户名/密码输入错误')
    update_last_login(None, ser.user)
    session_user_update(request, ser.user)
    res = dict(token=ser.validated_data.get('token'),
               user=UserSerializer(ser.user).data)
    return res


def token_user_password_change_handler(**kwrags):
    """用户根据id或者username+邮箱验证修改密码"""
    user_id = kwrags.get('id')
    res = dict(user=UserSerializer(user_id).data)
    # TODO:待开发
    pass


def get_username_field():
    try:
        User = get_user_model()
        username_field = User.USERNAME_FIELD
    except AttributeError:
        username_field = 'username'

    return username_field


def token_user_info_handler(token):
    """
    date通过token获取user的基本信息
    """
    # user_id = _token_get_user_id(token)
    # 查询
    # print(REQUEST)
    _user = token_get_user_model(token)
    res = dict(user=UserInfoSerializer(_user).data)
    params = dict(user_id=_user.id)
    # 查询角色信息
    role = get_role_via_user(params)
    roles = dict(roles=[_[0] for _ in role])
    res = dict(res, **roles)
    return res


def token_verify_handler(token):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    _user = token_get_user_model(token)
    res = dict(user=UserSerializer(_user).data)
    return res


def token_refresh_sliding_handler(token):
    """
    采用滑动式JSON网络TOKEN，并在TOKEN的刷新期限尚未到期时返回新的刷新版本。
    """
    ser = TokenRefreshSlidingSerializer(data={'token': token})
    try:
        ser.is_valid(raise_exception=True)
    except AssertionError as e:
        log.info('token校验出错')
        raise InvalidJwtToken(detail='token校验出错')
    res = dict(token=ser.validated_data.get('token'))
    return res


def token_obtain_pair_handler(username, password):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    ser = TokenObtainPairSerializer(
        data={get_username_field(): username, 'password': password})
    ser.is_valid(raise_exception=True)
    update_last_login(None, ser.user)
    res = dict(refresh=ser.validated_data.get('refresh'),
               access=ser.validated_data.get('access'),
               user=UserSerializer(ser.user).data
               )
    return res


def token_refresh_handler(refresh):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    ser = TokenRefreshSerializer(data={'refresh': refresh})
    ser.is_valid(raise_exception=True)
    res = dict(refresh=ser.validated_data.get('refresh'),
               access=ser.validated_data.get('access')
               )
    return res
