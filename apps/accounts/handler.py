#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 基于https://github.com/SimpleJWT/django-rest-framework-simplejwt 开发jwt-TOKEN验证脚手架
# __REFERENCES__ :
# __date__: 2020/10/10 14
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer, TokenObtainSlidingSerializer, TokenRefreshSlidingSerializer, TokenVerifySerializer
from .types import User
from apps.api_exception import InvalidJwtToken
import logging
log = logging.getLogger('apps')

def get_username_field():
    try:
        username_field = User.USERNAME_FIELD
    except AttributeError:
        username_field = 'username'

    return username_field

# NOTE:Untyped tokens do not verify the "token_type" claim.  This is useful when performing general validation of a token's signature and other properties which do not relate to the token's intended use.
# def token_verify_handler(token):
#     """
#     Takes a token and indicates if it is valid.  This view provides no
#     information about a token's fitness for a particular use.
#     """
#     ser = TokenVerifySerializer({'token': token})
#     ser.is_valid(raise_exception=True)
#     print(ser)


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
    res = dict(refresh=ser.validated_data.get('refresh'),
               access=ser.validated_data.get('access')
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
    res = dict(token=ser.validated_data.get('token')
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
