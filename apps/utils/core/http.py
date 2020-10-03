#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : http405报错判断
# __REFERENCES__ : F:\Envs\env\Lib\site-packages\django\views\decorators\http.py
# __date__: 2020/09/23 12

from apps.utils.wsme.signature import get_dataformat
# F:\Envs\env\Lib\site-packages\rest_framework\status.py
from rest_framework.status import  HTTP_405_METHOD_NOT_ALLOWED
from apps.apis.urls import urlpatterns
from django.http.response import HttpResponseNotAllowed
import logging
log = logging.getLogger('apps')
import json
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
        
        urlpatterns.append(url(r'^{path}/$'.format(path=path), inner, name=name))
        return inner
    return decorator


