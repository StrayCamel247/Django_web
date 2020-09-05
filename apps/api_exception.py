#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/16 17:18:43

from django.utils.translation import ugettext as _

UNDEFINED_EXCEPTION_CODE = 0x0000FFFF
UNDEFINED_EXCEPTION_MSG = _("System busy")

PRODUCT_MSG = _("System busy, please contact system admin or try again later")
PRODUCT_ERROR_CODE = 0x1f4

class ErrorCons:
    def __init__(self, **kwargs):
        if 'code' in kwargs.keys():
            self.code = kwargs['code']
        if 'msg' in kwargs.keys():
            self.msg = kwargs['msg']
        self.debuginfo = None

    def as_dict(self):
        return self.__dict__

class APIException(Exception):
    def __init__(self, msg=None, error_code=None):
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        print("%s :::: %d" % (caller.filename, caller.lineno))

        super(APIException, self).__init__(msg, None)
    
class DBAccessFail(APIException):
    msg = _('DB access failed')
    error_code = 0x00000001


class Fail(APIException):
    msg = _('Query failed')
    error_code = 0x00000002


class ParameterException(APIException):
    msg = _('Invalid parameter')
    error_code = 0x00000003


class ServerError(APIException):
    msg = _('The server is busy, please try again later')
    error_code = 0x00000004


class NotFound(APIException):
    msg = _('Request content does not exist')
    error_code = 0x00000005


class DBError(APIException):
    msg = _('The database is busy, please try again later')
    error_code = 0x00000006


class QueryError(APIException):
    msg = _('Query error')
    error_code = 0x00000007


class InvalidUser(APIException):
    msg = _("Invalid username or password")
    error_code = 0x00000008


class InvalidPassword(APIException):
    msg = _("Invalid username or password")
    error_code = 0x00000009


class UserExists(APIException):
    msg = _("This user already exists")
    error_code = 0x0000000A


class CaptchaError(APIException):
    msg = _("Captcha is error")
    error_code = 0x0000000B


class NoLegalPassword(APIException):
    msg = _("The password is not legal.")
    error_code = 0x0000000C


class NewNoLegalPassword(APIException):
    msg = _("The new password is not legal.")
    error_code = 0x0000000D


class DifferentPassword(APIException):
    msg = _("The password entered twice is different.")
    error_code = 0x0000000E


class InvalidUserMail(APIException):
    msg = _("Invalid user or mailbox")
    error_code = 0x0000000F


class InvalidCsrfToken(APIException):
    msg = _("Invalid csrf token")
    error_code = 0x00000010


class NeedLogin(APIException):
    msg = _("You need to sign in to use this feature")
    error_code = 0x00000011


class ResourceTypeExists(APIException):
    msg = _("The resource type already exists")
    error_code = 0x00000012


class ResourceNotEmpty(APIException):
    msg = _("The resource needs to be empty")
    error_code = 0x00000013


class ResourceTypeNotExists(APIException):
    msg = _("The resource type does not exist")
    error_code = 0x00000014


class ResourceNotExists(APIException):
    msg = _("The resource does not exist")
    error_code = 0xF00000015


class ResourceExists(APIException):
    msg = _("The resource already exists")
    error_code = 0x00000016


class RoleNotExists(APIException):
    msg = _("The role does not exist")
    error_code = 0x00000017


class UserForbidden(APIException):
    msg = _("The user already forbidden")
    error_code = 0x00000018


class IsExists(APIException):
    msg = _("This data already exists")
    error_code = 0x00000019


class FieldTypeError(APIException):
    msg = _("Field type error")
    error_code = 0x0000001A


class ResourceTypeMappingExists(APIException):
    msg = _("This resource_type_mapping already exists")
    error_code = 0x0000001B


class ResourceTypeMappingNotExists(APIException):
    msg = _("This resource_type_mapping not exists")
    error_code = 0x0000001C


class FieldEmptyError(APIException):
    msg = _("The field cannot be empty")
    error_code = 0x0000001D


class AttributeNotExist(APIException):
    msg = _("The resource attribute does not exist")
    error_code = 0x0000001F


class FieldLengthNotExist(APIException):
    msg = _("varchar type field length must exist")
    error_code = 0x00000020


class FileTypeError(APIException):
    msg = _("The file type error")
    error_code = 0x00000021


class InsufficientPermissionsError(APIException):
    msg = _("Insufficient permissions")
    error_code = 0x00000022


class RoleUsed(APIException):
    msg = _("This role is in use and cannot be deleted")
    error_code = 0x00000023


class UserUsed(APIException):
    msg = _("This user is in use and cannot be deleted")
    error_code = 0x00000024
