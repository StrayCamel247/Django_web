#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/16 15:35:10

import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import ugettext as _
from apps.api_exception import ParameterException

class ComputeSvmBody(wtypes.Base):
    minSupport = wsme.wsattr(float, default=0.3)
    max_k = wsme.wsattr(int, default=2)
    data = wsme.wsattr(_types.jsontype, mandatory=True)

    def validate(self):
        if not self.data:
            raise ParameterException(detail=str(_("params error")))
        # 检查输入的二维列表为二维，且每个元素为int
        try:
            check = sum(not isinstance(__, int) for _ in self.data for __ in _)
        except TypeError:
            raise ParameterException(detail=str(_("data维度必须是二维列表")))
        if check:
            raise ParameterException(detail=str(_("data元素必须为int")))
        return self

class ComputeFPgrowthBody(wtypes.Base):
    simpDat = wsme.wsattr(_types.jsontype, mandatory=True)
    minSupport = wsme.wsattr(float, default=2)

    def validate(self):
        if not self.simpDat:
            raise ParameterException(detail=str(_("params error")))
        # 检查输入的二维列表为二维，且每个元素为int
        try:
            check = sum(not isinstance(__, str)
                        for _ in self.simpDat for __ in _)
        except TypeError:
            raise ParameterException(detail=str(_("data维度必须是二维列表")))
        if check:
            raise ParameterException(detail=str(_("data元素必须为str")))
        return self


class ComputeAprioriBody(wtypes.Base):
    minSupport = wsme.wsattr(float, default=0.3)
    max_k = wsme.wsattr(int, default=2)
    data = wsme.wsattr(_types.jsontype, mandatory=True)

    def validate(self):
        if not self.data:
            raise ParameterException(detail=str(_("params error")))
        # 检查输入的二维列表为二维，且每个元素为int
        try:
            check = sum(not isinstance(__, int) for _ in self.data for __ in _)
        except TypeError:
            raise ParameterException(detail=str(_("data维度必须是二维列表")))
        if check:
            raise ParameterException(detail=str(_("data元素必须为int")))
        return self


class HelloWordResult(wtypes.Base):
    status_code = wsme.wsattr(int, default=200)
    content = _types.jsontype
    detail = wsme.wsattr(wtypes.text, default=str(_('success')))


class HelloWordBody(wtypes.Base):
    test = wsme.wsattr(wtypes.text, mandatory=True)

    def validate(self):
        if not self.test:
            raise ParameterException(detail=str(_("params error")))
        if self.test == "test":
            pass
        return self
