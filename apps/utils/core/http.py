#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : http405报错判断
# __REFERENCES__ : F:\Envs\env\Lib\site-packages\django\views\decorators\http.py
# __date__: 2020/09/23 12

from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf.urls import url
from apps.api_exception import ParameterException
import json
from apps.utils.wsme.signature import get_dataformat
# F:\Envs\env\Lib\site-packages\rest_framework\status.py
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from apps.apis.urls import urlpatterns
from django.http.response import HttpResponseNotAllowed
import logging
from apps.api_exception import InsufficientPermissionsError, NeedLogin
log = logging.getLogger('apps')


def check_user(user: 'checks that the user is logged in', perm: 'checks whether a user has a particular permission enabled' = None, raise_exception=True):
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


def require_http_methods(path, name=None, methods=[], **check):
    """
    用户指定view对应的url和request methods，并将url注册到apis连接下
    NOTE:
        @require_http_methods('data/iris_data', methods=['GET'])
        def my_view(request):
            # I can assume now that only GET or POST requests make it this far
    **check:
        login_required = True 开启校验
        perm = (user拥有的权限)
        指定访问url的user的限制
        参考:django/contrib/auth/decorators.py
    """
    if not path:
        raise ParameterException('请传入url')
    name = path if not name else name

    def decorator(func):
        def inner(request, *args, **kwargs):
            # methods校验
            try:
                assert request.method in methods
            except AssertionError:
                res = get_dataformat(request)
                message = 'Method Not Allowed ({method}): {path}'.format(
                    method=request.method, path=request.path)
                r = dict(status_code=HTTP_405_METHOD_NOT_ALLOWED,
                         detail=message)
                response = HttpResponseNotAllowed(
                    methods, json.dumps(r), content_type=res.content_type)
                log.warn(message)
                return response

            # user校验
            try:
                assert check.get('login_required') and check_user(
                    request.user, perm=check.get('perm'))
            except InsufficientPermissionsError:
                message = 'user get no permission (perm:{perm})'.format(
                    perm=check.get('perm'))
                raise InsufficientPermissionsError(detail=message)
            except AssertionError:
                message = 'user not authentication'
                raise NeedLogin(detail=message)

            return func(request, *args, **kwargs)

        urlpatterns.append(
            url(r'^{path}/$'.format(path=path), inner, name=name))
        return inner
    return decorator
