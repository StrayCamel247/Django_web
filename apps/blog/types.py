#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/10 15:04:18

import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import ugettext as _
from apps.api_exception import ParameterException
class BlogResult(wtypes.Base):
    status_code =  wsme.wsattr(int, default=0)
    content = _types.jsontype
    detail =  wsme.wsattr(wtypes.text, default=str(_('success')))

class BlogBody(wtypes.Base):
    test = wsme.wsattr(wtypes.text, mandatory=True)
    def validate(self):
        if not self.test :
            raise ParameterException(detail=str(_("params error")))
        if self.test == "test":
            pass
        return self


