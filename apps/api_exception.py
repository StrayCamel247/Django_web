#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/16 17:18:43

from apps.utils.wsme.signature import get_dataformat
import json
from django.http.response import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden,HttpResponseNotAllowed
from functools import lru_cache
import logging
import sys
import six
import traceback
from django.utils.translation import ugettext as _
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler, set_rollback
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
# F:\Envs\env\Lib\site-packages\rest_framework\status.py
from rest_framework.status import is_client_error, is_server_error
UNDEFINED_EXCEPTION_CODE = 0x000000FF
_HANDLER400_CODE = 0x190
_HANDLER403_CODE = 0x193
_HANDLER404_CODE = 0x194
_HANDLER500_CODE = 0x1f4
UNDEFINED_EXCEPTION_MSG = _("System busy")
log = logging.getLogger('apps')

PRODUCT_MSG = _("System busy, please contact system admin or try again later")
PRODUCT_ERROR_CODE = 0x1f4


@lru_cache(maxsize=128, typed=False)
def _exception_handler(exc, debug=True):
    """Extract informations that can be sent to the client."""
    status_code = getattr(exc[0], 'status_code', None)
    if status_code:
        detail = (six.text_type(exc[0].detail) if hasattr(exc[0], 'detail')
                  else six.text_type(exc))
        r = dict(status_code=status_code,
                 detail=UNDEFINED_EXCEPTION_MSG)
        # log.warn("Defined error: %s" % r['detail'])
        r['debuginfo'] = detail
        return Response(r)
    else:
        detail = six.text_type(exc)
        excinfo = sys.exc_info()
        debuginfo = "\n".join(traceback.format_exception(*excinfo))

        log.error('Undefined error: "%s". detail: \n%s' % (
            detail, debuginfo))
        # TODO:待开发，异步发送邮件
        # send_mail(detail, debuginfo, settings.DEFAULT_FROM_EMAIL,
        #           ['aboyinsky@outlook.com'])
        r = dict(status_code=UNDEFINED_EXCEPTION_CODE,
                 detail=six.text_type(UNDEFINED_EXCEPTION_MSG))
        if debug:
            r['debuginfo'] = detail
        else:
            r['debuginfo'] = None
        set_rollback()
        return Response(r, status=UNDEFINED_EXCEPTION_CODE)


def _handler400(request=None, exception=None):
    response = exception_handler(
        exc=exception, context=None)
    pass


def _handler403(request=None, exception=None):
    """重写django系统对400、403、404、500code报错的机制handler"""
    response = exception_handler(
        exc=exception, context=None)
    res = get_dataformat(request)
    response.data['debuginfo'] = repr(exception)
    log.error(repr(exception))
    response.data['status_code'] = _HANDLER403_CODE
    return HttpResponseForbidden(json.dumps(response.data), content_type=res.content_type)


def _handler404(request=None, exception=None):
    """重写django系统对400、403、404、500code报错的机制handler"""
    response = exception_handler(
        exc=exception, context=None)
    res = get_dataformat(request)
    args = exception.args
    for _ in args:
        # 404报错会在tried中返回所有的路由，隐私关系我们只返回'all_modules'
        if _.get('tried'):
            _['tried'] = 'all_modules'
    response.data['debuginfo'] = repr(exception)
    log.error(repr(exception))
    response.data['status_code'] = _HANDLER404_CODE
    return HttpResponseNotFound(json.dumps(response.data), content_type=res.content_type)


    
def _handler500(request=None, exception=None):
    """重写django系统对400、403、404、500code报错的机制handler"""
    exception = sys.exc_info()
    response = exception_process(
        exception=exception, context=None)
    res = get_dataformat(request)
    response.data['status_code']= _HANDLER500_CODE
    print(res)
    return HttpResponseServerError(json.dumps(response.data), content_type=res.content_type)


def exception_process(request=None, exception=None, context=None):
    # 获取本restful_framwork返回的exception的
    response = exception_handler(
        exc=exception, context=context)
    # 没有获取response 走本地路由
    if not response:
        exception_info = sys.exc_info()
        response = _exception_handler(exception_info, debug=True)
    response.data['status_code'] = response.status_code
    return response


class DBAccessFail(APIException):
    detail = _('DB access failed')
    status_code = 0x00000001


class Fail(APIException):
    detail = _('Query failed')
    status_code = 0x00000002


class ParameterException(APIException):
    detail = _('Invalid parameter')
    status_code = 0x00000003


class ServerError(APIException):
    detail = _('The server is busy, please try again later')
    status_code = 0x00000004


class NotFound(APIException):
    detail = _('Request content does not exist')
    status_code = 0x00000005


class DBError(APIException):
    detail = _('The database is busy, please try again later')
    status_code = 0x00000006


class QueryError(APIException):
    detail = _('Query error')
    status_code = 0x00000007


class InvalidUser(APIException):
    detail = _("Invalid username or password")
    status_code = 0x00000008


class InvalidPassword(APIException):
    detail = _("Invalid username or password")
    status_code = 0x00000009


class UserExists(APIException):
    detail = _("This user already exists")
    status_code = 0x0000000A


class CaptchaError(APIException):
    detail = _("Captcha is error")
    status_code = 0x0000000B


class NoLegalPassword(APIException):
    detail = _("The password is not legal.")
    status_code = 0x0000000C


class NewNoLegalPassword(APIException):
    detail = _("The new password is not legal.")
    status_code = 0x0000000D


class DifferentPassword(APIException):
    detail = _("The password entered twice is different.")
    status_code = 0x0000000E


class InvalidUserMail(APIException):
    detail = _("Invalid user or mailbox")
    status_code = 0x0000000F


class InvalidJwtToken(APIException):
    detail = _("Invalid jwt token")
    status_code = 0x00000010

# class InvalidCsrfToken(APIException):
#     detail = _("Invalid csrf token")
#     status_code = 0x00000010


class NeedLogin(APIException):
    detail = _("You need to sign in to use this feature")
    status_code = 0x00000011


class ResourceTypeExists(APIException):
    detail = _("The resource type already exists")
    status_code = 0x00000012


class ResourceNotEmpty(APIException):
    detail = _("The resource needs to be empty")
    status_code = 0x00000013


class ResourceTypeNotExists(APIException):
    detail = _("The resource type does not exist")
    status_code = 0x00000014


class ResourceNotExists(APIException):
    detail = _("The resource does not exist")
    status_code = 0xF00000015


class ResourceExists(APIException):
    detail = _("The resource already exists")
    status_code = 0x00000016


class RoleNotExists(APIException):
    detail = _("The role does not exist")
    status_code = 0x00000017


class UserForbidden(APIException):
    detail = _("The user already forbidden")
    status_code = 0x00000018


class IsExists(APIException):
    detail = _("This data already exists")
    status_code = 0x00000019


class FieldTypeError(APIException):
    detail = _("Field type error")
    status_code = 0x0000001A


class ResourceTypeMappingExists(APIException):
    detail = _("This resource_type_mapping already exists")
    status_code = 0x0000001B


class ResourceTypeMappingNotExists(APIException):
    detail = _("This resource_type_mapping not exists")
    status_code = 0x0000001C


class FieldEmptyError(APIException):
    detail = _("The field cannot be empty")
    status_code = 0x0000001D


class AttributeNotExist(APIException):
    detail = _("The resource attribute does not exist")
    status_code = 0x0000001F


class FieldLengthNotExist(APIException):
    detail = _("varchar type field length must exist")
    status_code = 0x00000020


class FileTypeError(APIException):
    detail = _("The file type error")
    status_code = 0x00000021


class InsufficientPermissionsError(APIException):
    detail = _("Insufficient permissions")
    status_code = 0x00000022


class RoleUsed(APIException):
    detail = _("This role is in use and cannot be deleted")
    status_code = 0x00000023


class UserUsed(APIException):
    detail = _("This user is in use and cannot be deleted")
    status_code = 0x00000024

class ResponseNotAllowed(APIException):
    detail = _("'Method Not Allowed")
    status_code = 0x00000195