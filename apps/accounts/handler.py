#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 基于https://github.com/SimpleJWT/django-rest-framework-simplejwt 开发jwt-TOKEN验证脚手架
# __REFERENCES__ :
# __date__: 2020/10/10 14
import inspect
import logging
import re
from datetime import date

from apps.api_exception import InvalidJwtToken, InvalidUser
from apps.apis.serializers import UserSerializer
from apps.role.models import get_role_via_user
from apps.utils.core.http import REQUEST
from apps.utils.email.handler import send_email
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth import (BACKEND_SESSION_KEY, HASH_SESSION_KEY,
                                 SESSION_KEY, get_user, get_user_model)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import (user_logged_in, user_logged_out,
                                         user_login_failed)
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare
from django.utils.module_loading import import_string
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenObtainSlidingSerializer,
    TokenRefreshSerializer, TokenRefreshSlidingSerializer,
    TokenVerifySerializer)

from .models import UserInfoSerializer, token_get_user_model
from .types import User

log = logging.getLogger('apps')


def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])


def logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()


def login(request, user, backend=None):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                session_auth_hash and
                not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    try:
        backend = backend or user.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                'You have multiple authentication backends configured and '
                'therefore must provide the `backend` argument or set the '
                '`backend` attribute on the user.'
            )
    else:
        if not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).' % backend)

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)

# 修改密码


def token_user_password_change_handler(**kwrags):
    """用户根据id或者username+邮箱验证修改密码"""
    user_id = kwrags.get('id')
    res = dict(user=UserSerializer(user_id).data)
    # TODO:待开发
    pass


def get_username_field():
    try:
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


def token_obtain_sliding_logout_handler():
    """
    用户登出，更新用户信息，注销request信息等
    """
    try:
        log.info(REQUEST)
        current_request = REQUEST.get('current_request', None)
        assert current_request
        logout(current_request)
    except Exception as e:
        log.warn(e)
    return '登出成功'


def token_obtain_sliding_login_handler(username, password):
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
    print(REQUEST)
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
