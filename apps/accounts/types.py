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

class AccountsResult(wtypes.Base):
    status_code = wsme.wsattr(int, default=200)
    content = _types.jsontype
    detail = wsme.wsattr(wtypes.text, default=str(_('success')))


class AccountLoginBody(wtypes.Base):
    username = wsme.wsattr(wtypes.text, mandatory=True)
    password = wsme.wsattr(wtypes.text, mandatory=True)

    def validate(self):
        if not self.username:
            raise ParameterException(detail=str(_("params error")))
        if self.username == "username":
            pass
        return self
