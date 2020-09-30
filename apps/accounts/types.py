#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 
# __REFERENCES__ : 
# __date__: 2020/09/28 12
import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import ugettext as _
from apps.api_exception import ParameterException

class AccountTokenBody(wtypes.Base):
    token = wsme.wsattr(wtypes.text, mandatory=True)

    def validate(self):
        if not len(self.token.split('.')) ==3:
            raise ParameterException('token应该包含 Header（头部）.Payload（负载）.Signature（签名）三个部分')
        return self

class AccountLoginBody(wtypes.Base):
    username = wsme.wsattr(wtypes.text, mandatory=True)
    password = wsme.wsattr(wtypes.text, mandatory=True)

    def validate(self):
        return self

class AccountsResult(wtypes.Base):
    status_code = wsme.wsattr(int, default=200)
    content = _types.jsontype
    detail = wsme.wsattr(wtypes.text, default=str(_('success')))

    def validate(self):
        print('test')
        return self


