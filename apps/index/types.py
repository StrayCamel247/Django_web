#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/16 15:35:10

import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import ugettext as _

class HelloResult(wtypes.Base):
    code = wsme.wsattr(int, default=0)
    msg = wsme.wsattr(wtypes.text, default=str(_('success')))
    content = _types.jsontype

class HelloBody(wtypes.Base):
    test = wsme.wsattr(wtypes.text, mandatory=True)

    def validate(self):
        if not self.test :
            raise ParameterException(msg=str(_("params error")))
        if self.test == "test":
            pass
        return self
