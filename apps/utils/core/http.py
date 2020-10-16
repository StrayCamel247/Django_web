#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : http405报错判断
# __REFERENCES__ :
# __date__: 2020/09/23 12

from django.conf.urls import url
from django.template.base import kwarg_re
from django.http.response import HttpResponseNotAllowed
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from apps.api_exception import ParameterException
from apps.utils.wsme.signature import get_dataformat
# F:\Envs\env\Lib\site-packages\rest_framework\status.py
from apps.apis.urls import urlpatterns
from apps.api_exception import InsufficientPermissionsError, NeedLogin, InvalidJwtToken, ResponseNotAllowed
from apps.accounts.handler import token_get_user_model
import logging
import json
import functools
log = logging.getLogger('apps')
from django.core.handlers.wsgi import WSGIRequest 
# 去安居request,针对 传入token的url 赋值此request，具体引用方法看apps\data\views.py
request = None


def require_http_methods(path, name=None, methods:
                         "用户指定url和request methods，并将url注册到apis连接下" = [], login_required: "用户指定是否开启request.user校验" = False, perm: "user拥有的权限" = (), jwt_required: "用户指定是否开启request.jwt校验" = False, **check):
    """
        指定访问url的user的限制
        参考:django/contrib/auth/decorators.py; django/views/decorators/http.py
    """
    if not path:
        raise ParameterException('请传入url')
    name = path if not name else name
    
    def decorator(func):
        @functools.wraps(func)
        def inner(req,*args, **kwargs):
            # methods校验
            methods_check(req, methods)
            # req.user校验
            request_user_check(req, login_required, perm)
            # NOTE:推荐
            # req.token校验，更新token并通过接口返回
            res = request_token_check(
                req, func, jwt_required, *args, **kwargs)
            
            # 邮箱验证
            res = request_token_check(
                req, func, jwt_required, *args, **kwargs)
            return res if res else func(req, *args, **kwargs)

        urlpatterns.append(
            url(r'^{path}/$'.format(path=path), inner, name=name))
        return inner
    return decorator


def user_check(user: 'checks that the user is logged in', perm: 'checks whether a user has a particular permission enabled' = None, raise_exception=True):
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
    try:
        assert req.method in methods
    except AssertionError:
        message = 'Method Not Allowed ({method}): {path}'.format(
            method=req.method, path=req.path)
        log.warning(message)
        raise ResponseNotAllowed(detail=message)


def request_user_check(req, login_required, perm):
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


def update_request(req, **kwargs):
    """修改request属性，并同步到全局变量"""
    global request
    for k, v in kwargs.items():
        setattr(req, k, v)
    request = req
    print(request)
    return req


def request_token_check(req, func, jwt_required, *args, **kwargs):
    """校验token，获取user信息并添加到request中"""
    try:
        assert jwt_required
        token = req.headers._store.get('token')[1]
        user = token_get_user_model(token)
        # 讲登陆后的user 插入request中
        req = update_request(req, user=user)
        res = func(req, *args, **kwargs)
        res.content = json.dumps(
            dict(json.loads(res.content)))
        return res
    except AssertionError:
        pass
    except IndexError:
        message = 'headers need token'
        log.warn(message)
        raise InvalidJwtToken(detail=message)
    except:
        message = 'user not authentication'
        log.warn(message)
        raise InvalidJwtToken(detail=message)
