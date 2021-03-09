#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 基于https://github.com/SimpleJWT/django-rest-framework-simplejwt 开发jwt-TOKEN验证脚手架
# __REFERENCES__ :
# __date__: 2020/10/10 14
import logging
from apps.api_exception import ParameterException
from django.contrib.auth import (BACKEND_SESSION_KEY, HASH_SESSION_KEY,
                                 SESSION_KEY, get_user_model, _get_backends)
from django.utils.crypto import constant_time_compare
import six
import os
env = os.getenv('django_web_flag', 'loc')


def session_logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', True):
        user = None
    # user_logged_out.send(sender=user.__class__, request=request, user=user)
    # login check
    session_key = getattr(request.session, 'session_key', None)
    from django.contrib.sessions.models import Session
    try:
        session = Session.objects.get(session_key=session_key)
        assert getattr(session, 'pk')
    except Exception as e:
        logging.info(six.text_type(e))
        raise ParameterException(detail='Pls login in first!')
    """
    session.flush()和session.clear()就针对session的一级缓存的处理。

    简单的说，

    1 session.flush()的作用就是将session的缓存中的数据与数据库同步。

    2 session.clear()的作用就是清除session中的缓存数据（不管缓存与数据库的同步）。
    执行完session.flush()时，并不意味着数据就肯定持久化到数据库中的，因为事务控制着数据库，如果事务提交失败了，缓存中的数据还是照样会被回滚的。
    """
    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()


def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])


def session_user_update(request, user=None, backend=None):
    """
    根据session更新用户信息
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
        if len(backends) == 1 or env == 'loc':
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
    # update_request(request)
    # user_logged_in.send(sender=user.__class__, request=request, user=user)
