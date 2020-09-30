#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 
# __REFERENCES__ : 
# __date__: 2020/09/30 08
import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import ugettext as _
from apps.api_exception import ParameterException
class JWTResult(wtypes.Base):
    code = wsme.wsattr(int, default=0)
    content = _types.jsontype
    msg = wsme.wsattr(wtypes.text, default=str(_('success')))

class JWTLoginBody(wtypes.Base):
    test = wsme.wsattr(wtypes.text, mandatory=True)
    def validate(self):
        if not self.test :
            raise ParameterException(msg=str(_("params error")))
        if self.test == "test":
            pass
        return self
