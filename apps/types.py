#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/10 15:05:24


import json
from django.utils.translation import ugettext as _

from oslo_utils import strutils
from oslo_utils import uuidutils
import six
import wsme
import wsme.types as wtypes

from apps import api_exception


class UuidType(wtypes.UserType):
    """A simple UUID type."""

    basetype = wtypes.text
    name = 'uuid'

    @staticmethod
    def validate(value):
        if not uuidutils.is_uuid_like(value):
            raise api_exception.ParameterException()
        return value

    @staticmethod
    def frombasetype(value):
        if value is None:
            return None
        return UuidType.validate(value)


class BooleanType(wtypes.UserType):
    """A simple boolean type."""

    basetype = wtypes.text
    name = 'boolean'

    @staticmethod
    def validate(value):
        try:
            return strutils.bool_from_string(value, strict=True)
        except ValueError as e:
            # raise Invalid to return 400 (BadRequest) in the API
            raise api_exception.ParameterException(six.text_type(e))

    @staticmethod
    def frombasetype(value):
        if value is None:
            return None
        return BooleanType.validate(value)


class JsonType(wtypes.UserType):
    """A simple JSON type."""

    basetype = wtypes.text
    name = 'json'

    def __str__(self):
        # These are the json serializable native types
        return ' | '.join(map(str, (wtypes.text, six.integer_types, float,
                                    BooleanType, list, dict, None)))

    @staticmethod
    def validate(value):
        try:
            json.dumps(value)
        except TypeError:
            raise api_exception.ParameterException(('%s is not JSON serializable') % value)
        else:
            return value

    @staticmethod
    def frombasetype(value):
        return JsonType.validate(value)


class ListType(wtypes.UserType):
    """A simple list type."""

    basetype = wtypes.text
    name = 'list'

    @staticmethod
    def validate(value):
        """Validate and convert the input to a ListType.

        :param value: A comma separated string of values
        :returns: A list of unique values (lower-cased), maintaining the
                  same order
        """
        if isinstance(value, list):
            return value
        else:
            raise api_exception.ParameterException(msg='应该传数组类型')

    @staticmethod
    def frombasetype(value):
        if value is None:
            return None
        return ListType.validate(value)


uuid = UuidType()
boolean = BooleanType()
listtype = ListType()
# Can't call it 'json' because that's the name of the stdlib module
jsontype = JsonType()


class Base(wtypes.Base):
    def as_dict_from_keys(self, keys):
        return dict((k, getattr(self, k))
                    for k in keys
                    if hasattr(self, k) and
                    getattr(self, k) != wsme.Unset)

    def as_dict(self):
        keys = [i for i in self.__class__.__dict__.keys() if i[:1] != '_']
        return self.as_dict_from_keys(keys)


class BaseResult(wtypes.Base):
    code = wsme.wsattr(int, default=0)


class FailResult(BaseResult):
    code = wsme.wsattr(wtypes.text, default=0xFFFF1111)
    msg = wsme.wsattr(wtypes.text, default=str(_('Fail')))
    content = jsontype

class Success(BaseResult):
    msg = wtypes.text


class QueryFlatResult(BaseResult):
    content = jsontype


class QueryFormatResult(BaseResult):
    content = jsontype