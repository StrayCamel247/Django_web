#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : http405报错判断
# __REFERENCES__ :
# __date__: 2020/09/23 12

import functools
import json
import logging

from apps.accounts.models import token_get_user_model
from apps.api_exception import (InsufficientPermissionsError, InvalidJwtToken,
                                InvalidUser, ParameterException,
                                ResponseNotAllowed)
# F:\Envs\env\Lib\site-packages\rest_framework\status.py
from apps.apis.urls import urlpatterns
from django.conf.urls import url

log = logging.getLogger('apps')
# request,针对 传入token的url 赋值此request，具体引用方法看apps\data\views.py
# TODO: 将用户访问的请求作成队列保存到数据库
REQUEST = {'current_request': None}


def require_http_methods(path, name=None,
                         methods: "用户指定url和request methods，并将url注册到apis连接下" = [],
                         login_required: "用户指定是否开启request.user校验" = False,
                         perm: "user拥有的权限" = (),
                         jwt_required: "用户指定是否开启request.jwt校验" = False,
                         ini_request: "初始化request，即可通过from apps.utils.core.http import REQUEST 引用当前request" = False,
                         **check):
    """
        指定访问url的user的限制
        参考:django/contrib/auth/decorators.py; django/views/decorators/http.py
    """
    if not path:
        raise ParameterException('请传入url')
    name = path if not name else name

    def decorator(func):
        @functools.wraps(func)
        def inner(req, *args, **kwargs):
            # methods校验
            methods_check(req, methods)
            # NOTE:暂时弃用，req.user校验
            # request_ckeck(req, login_required, ini_request, perm)
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
    try:
        assert req.method in methods
    except AssertionError:
        message = 'Method Not Allowed ({method}): {path}'.format(
            method=req.method, path=req.path)
        log.warning(message)
        raise ResponseNotAllowed(detail=message)


def request_ckeck(req, login_required, ini_request, perm):
    # 登陆校验
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
    # request更新
    try:
        assert ini_request
        global REQUEST
        REQUEST['current_request'] = req
    except:
        pass


def update_request(req, **kwargs):
    """修改request属性，并同步到全局变量"""
    for k, v in kwargs.items():
        setattr(req, k, v)
    global REQUEST
    REQUEST['current_request'] = req
    return req


def request_token_check(req, func, jwt_required, *args, **kwargs):
    """校验token，获取user信息并添加到request中"""
    try:
        assert jwt_required
        token = req.headers._store.get('token')[1]
        user = token_get_user_model(token)
        # 验证session中user是否匹配
        from django.contrib.auth import get_user
        _user = get_user(req)
        if not user.pk == _user.pk:
            raise InvalidUser(detail='session和token不匹配')
        # 将登陆后的user 插入request中
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
    except Exception as e:
        message = 'user not authentication'
        log.warn(e)
        raise InvalidJwtToken(detail=message)
