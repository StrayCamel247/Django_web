#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 获取模型需要训练的数据集，只获取不修改，构建redis/pickle缓存系统，尽可能自动下载数据集并缓存。
# __REFERENCES__ :
# __date__: 2020/09/27 16

import re

from django.http import request
from apps.utils.wsme.signature import signature
from apps.utils.core.http import require_http_methods
from .types import DashboardResult, KpiBody
from .handler import KpiFactory, generate_transaction_list, kpi_indicator_handler,get_dashboard_barChart_handler
# url锚点，让config.urls中集合url的机制可以访问到，并调用require_http_methods将url注册到apis中，和restful接口相集合
urlpatterns = []


@require_http_methods('dashboard/indicator', methods=['GET'])
@signature(DashboardResult)
def kpi_indicator(request):
    """查询前端展示的kpi 指标"""
    params = dict(
        request=request,
    )
    result = kpi_indicator_handler(**params)
    return DashboardResult(content=result)


@require_http_methods('dashboard/kpi_value', methods=['POST'])
@signature(DashboardResult, body=KpiBody)
def kpi_value(request,body):
    """kpi值接口  根据 indicator 传入参数不同请求不同的 handler"""
    params = {
        "indicator": body.indicator
    }
    handler = KpiFactory().create_handler(params["indicator"])
    result = handler(params=params)
    return DashboardResult(content=result)


@require_http_methods('transaction/list', methods=['GET'])
@signature(DashboardResult, int)
def iris_data_view(request,page):
    """制造假数据"""
    data = generate_transaction_list(page=page)
    res = DashboardResult(content=data)
    return res

@require_http_methods('dashboard/barChart', methods=['POST'])
@signature(DashboardResult)
def kpi_value(request):
    # TODO:假数据
    result = get_dashboard_barChart_handler()
    return DashboardResult(content=result)