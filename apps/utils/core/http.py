#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : http405报错判断
# __REFERENCES__ : F:\Envs\env\Lib\site-packages\django\views\decorators\http.py
# __date__: 2020/09/23 12

from functools import wraps
from apps.utils.wsme.signature import get_dataformat
# F:\Envs\env\Lib\site-packages\rest_framework\status.py
from rest_framework.status import is_client_error, is_server_error, HTTP_405_METHOD_NOT_ALLOWED
from config.urls import urlpatterns
from django.http.response import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
import logging
log = logging.getLogger('apps')
import json, sys
from apps.api_exception import ParameterException
from django.conf.urls import url

def require_http_methods(path, name=None, methods=[]):
    """
    Decorator to make a view only accept particular request methods.  Usage::

        @require_http_methods(["GET", "POST"])
        def my_view(request):
            # I can assume now that only GET or POST requests make it this far
            # ...

    Note that request methods should be in uppercase.
    """
    if not path:
        raise ParameterException('请传入url')
    name = path if not name else name
    def decorator(func):
        urlpatterns.append(url(r'^apis/v1.0/{path}/$'.format(path=path), func, name=name))
        def inner(request, *args, **kwargs):
            if request.method not in methods:
                res = get_dataformat(request)
                message = 'Method Not Allowed ({method}): {path}'.format( method=request.method, path=request.path)
                r = dict(status_code=HTTP_405_METHOD_NOT_ALLOWED,
                         detail=message)
                response = HttpResponseNotAllowed(
                    methods, json.dumps(r), content_type=res.content_type)
                log.warn(message)
                return response
            return func(request, *args, **kwargs)
        return inner
    return decorator


# require_GET = require_http_methods(["GET"])
# require_GET.__doc__ = "Decorator to require that a view only accepts the GET method."

# require_POST = require_http_methods(["POST"])
# require_POST.__doc__ = "Decorator to require that a view only accepts the POST method."

# require_safe = require_http_methods(["GET", "HEAD"])
# require_safe.__doc__ = "Decorator to require that a view only accepts safe methods: GET and HEAD."
