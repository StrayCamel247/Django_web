#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 12:40:21

from apps.utils.wsme.signature import signature
from apps.utils.core.http import require_http_methods
from .types import HelloWordResult, ComputeAprioriBody, ComputeFPgrowthBody
from .moduls.apriori.hander import apriori
from .moduls.FPgrowth.handler import ft_growth

# url锚点，让config.urls中集合url的机制可以访问到，并调用require_http_methods将url注册到apis中，和restful接口相集合
urlpatterns=[]
@require_http_methods('data_analysis/compute_fp_growth', methods=['POST'])
@signature(HelloWordResult, body=ComputeFPgrowthBody)
def compute_fp_growth_view(request, body):
    params = {
        'simpDat': body.simpDat,
        'minSupport': body.minSupport
    }
    content = ft_growth(params)
    res = HelloWordResult(content=content)
    return res


@require_http_methods('data_analysis/compute_apriori', methods=['POST'])
@signature(HelloWordResult, body=ComputeAprioriBody)
def compute_apriori_view(request, body):
    params = {
        'data': body.data,
        'minSupport': body.minSupport,
        'max_k': body.max_k
    }
    content = apriori(params)
    res = HelloWordResult(content=content)
    return res

@require_http_methods('data_analysis/iris_svm', methods=['POST'])
@signature(HelloWordResult, body=ComputeAprioriBody)
def compute_apriori_view(request, body):
    params = {
        'minSupport': body.minSupport,
        'max_k': body.max_k
    }
    content = apriori(params)
    res = HelloWordResult(content=content)
    return res