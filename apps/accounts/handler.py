#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 基于https://github.com/SimpleJWT/django-rest-framework-simplejwt 开发jwt-TOKEN验证脚手架
# __REFERENCES__ :
# __date__: 2020/10/10 14
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer, TokenObtainSlidingSerializer, TokenRefreshSlidingSerializer, TokenVerifySerializer
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import SlidingToken
from rest_framework_simplejwt.models import TokenUser
from apps.api_exception import InvalidJwtToken
from apps.apis.serializers import UserSerializer
from .types import User
import logging
log = logging.getLogger('apps')


def get_username_field():
    try:
        username_field = User.USERNAME_FIELD
    except AttributeError:
        username_field = 'username'

    return username_field


def token_get_user_model(token):
    """
    Returns a stateless user object which is backed by the given validated
    token.
    """
    Token = SlidingToken(token)
    if api_settings.USER_ID_CLAIM not in Token:
        # The TokenUser class assumes tokens will have a recognizable user
        # identifier claim.
        raise InvalidJwtToken(
            'Token contained no recognizable user identification')
    log.info('验证token:{}，user_id为'.format(token, TokenUser(Token).id))
    _user = User.objects.get(id=TokenUser(Token).id)
    return _user


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


def token_obtain_sliding_handler(username, password):
    """
    Takes a set of user credentials and returns a sliding JSON web token to
    prove the authentication of those credentials.
    """
    ser = TokenObtainSlidingSerializer(
        data={get_username_field(): username, 'password': password})
    ser.is_valid(raise_exception=True)
    update_last_login(None, ser.user)
    res = dict(token=ser.validated_data.get('token'),
               user=UserSerializer(ser.user).data)
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
