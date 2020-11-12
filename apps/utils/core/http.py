#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : http405报错判断
# __REFERENCES__ :
# __date__: 2020/09/23 12

import os
import functools
import logging

import six
from apps.accounts.models import token_get_user_model
from apps.api_exception import (InsufficientPermissionsError, InvalidJwtToken,
                                InvalidUser, ParameterException,
                                ResponseNotAllowed)
# F:\Envs\env\Lib\site-packages\rest_framework\status.py
from apps.apis.urls import urlpatterns
from django.conf.urls import url

log = logging.getLogger('apps')
# request,针对 传入token的url 赋值此request，具体引用方法看apps\data\views.py

env = os.getenv('APPS_ENV', 'local')


def require_http_methods(path, name=None,
                         methods: "用户指定url和request methods，并将url注册到apis连接下" = [],
                         login_required: "用户指定是否开启request.user校验" = False,
                         perm: "user拥有的权限" = (),
                         jwt_required: "用户指定是否开启request.jwt校验" = True,
                         **check):
    """
        指定访问url的user的限制
        参考:django/contrib/auth/decorators.py; django/views/decorators/http.py
    """
    if not path:
        raise ParameterException('请传入url')

    def decorator(func):
        @functools.wraps(func)
        def inner(req, *args, **kwargs):
            # methods校验
            methods_check(req, methods)
            # request_ckeck(req, login_required, perm)
            request_token_check(
                req, func, jwt_required, *args, **kwargs)
            return func(req, *args, **kwargs)

        urlpatterns.append(
            url(
                r'^{path}$'.format(path=path), inner,
                name='{n}_defined in {p} via {m}'.format(
                    n=name or '',
                    p=path,
                    m=str(methods))
            )
        )
        return inner
    return decorator


def user_check(user: 'checks that the user is logged in',
               perm: 'checks whether a user has a particular permission enabled' = None,
               raise_exception=True):
    """校验request中的user"""
    if not perm:
        return user.is_authenticated
    if isinstance(perm, str):
        perms = (perm,)
    else:
        perms = perm
    # First check if the user has the permission (even anon users)
    if user.has_perms(perms):
        return True
    # In case the 403 handler should be called raise the exception
    if raise_exception:
        raise InsufficientPermissionsError
    # As the last resort, show the login form
    return False


def methods_check(req, methods):
    """
    接口请求方式校验
    """
    try:
        assert req.method in methods
    except AssertionError:
        message = 'Method Not Allowed ({method}): {path}'.format(
            method=req.method, path=req.path)
        log.warning(message)
        raise ResponseNotAllowed(detail=message)


def request_ckeck(req, login_required, perm):
    """
    登陆校验
    NOTE:暂时弃用，req.user校验
    """
    try:
        assert login_required
        user_check(req.user, perm)
    except AssertionError:
        pass
    except InsufficientPermissionsError:
        message = 'user get no permission (perm:{perm})'.format(
            perm=perm)
        log.warn(message)
        raise InsufficientPermissionsError(detail=message)


def request_token_check(req, func, jwt_required, *args, **kwargs):
    """校验token，获取user信息并添加到request中"""
    res = None
    # 本地环境无需验证登陆
    jwt_required *= env != 'local'
    try:
        assert jwt_required
        # 获取jwt中的user
        token = req.headers._store.get('x-token', (None, None))[1]
        user = token_get_user_model(token)
        # 获取session中的user
        from django.contrib.auth import get_user
        _user = get_user(req)
        # 校验user
        assert user.pk == _user.pk, 'session和token不匹配'
        # res = func(req, *args, **kwargs)
        # res.content = json.dumps(
        #     dict(json.loads(res.content)))
    except AssertionError as e:
        msg = six.text_type(e)
        if msg:
            raise InvalidUser('token和session用户不一致')
    except IndexError or TypeError:
        message = 'headers need token'
        log.warn(message)
        raise InvalidJwtToken(detail=message)
