#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 12:40:21

from django.views import generic
from apps.utils.wsme.signature import signature
from .types import HelloWordResult, ComputeAprioriBody, ComputeFPgrowthBody
from .models.apriori.hander import apriori
from .models.FPgrowth.handler import ft_growth
from apps.utils.core.http import require_http_methods


@require_http_methods('/data_analysis/compute_fp_growth', methods=['POST'])
@signature(HelloWordResult, body=ComputeFPgrowthBody)
def compute_fp_growth_view(body):
    params = {
        'simpDat': body.simpDat,
        'minSupport': body.minSupport
    }
    content = ft_growth(params)
    res = HelloWordResult(content=content)
    return res


@require_http_methods('/data_analysis/compute_apriori', methods=['POST'])
@signature(HelloWordResult, body=ComputeAprioriBody)
def compute_apriori_view(body):
    params = {
        'data': body.data,
        'minSupport': body.minSupport,
        'max_k': body.max_k
    }
    content = apriori(params)
    res = HelloWordResult(content=content)
    return res
