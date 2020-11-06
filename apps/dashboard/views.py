#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 获取模型需要训练的数据集，只获取不修改，构建redis/pickle缓存系统，尽可能自动下载数据集并缓存。
# __REFERENCES__ :
# __date__: 2020/09/27 16

import re


from apps.utils.wsme.signature import signature
from apps.utils.core.http import require_http_methods
from .types import DashboardResult, KpiBody
from .handler import KpiFactory, generate_transaction_list, kpi_indicator_handler, get_dashboard_barChart_handler,get_dashboard_BoxCard_handler
# url锚点，让config.urls中集合url的机制可以访问到，并调用require_http_methods将url注册到apis中，和restful接口相集合
urlpatterns = []


@require_http_methods('dashboard/indicator', methods=['GET'])
@signature(DashboardResult)
def kpi_indicator(request):
    """前端查询展示的kpi 指标"""
    params = dict(
        request=request,
    )
    result = kpi_indicator_handler(**params)
    return DashboardResult(content=result)


@require_http_methods('dashboard/kpi_value', methods=['POST'])
@signature(DashboardResult, body=KpiBody)
def kpi_value(request, body):
    """kpi值接口  根据 indicator 传入参数不同请求不同的 handler"""
    params = {
        "indicator": body.indicator
    }
    handler = KpiFactory().create_handler(params["indicator"])
    result = handler(params=params)
    return DashboardResult(content=result)


@require_http_methods('dashboard/TransactionTable', methods=['GET'])
@signature(DashboardResult, int)
def dashboard_TransactionTable(request, page):
    """前端查询展示dashboard/TransactionTable"""
    data = generate_transaction_list(page=page)
    res = DashboardResult(content=data)
    return res


@require_http_methods('dashboard/barChart', methods=['POST'])
@signature(DashboardResult)
def dashboard_barChart(request):
    """前端查询展示dashboard/barChart"""
    result = get_dashboard_barChart_handler()
    return DashboardResult(content=result)


@require_http_methods('dashboard/BoxCard', methods=['POST'])
@signature(DashboardResult)
def dashboard_BoxChart(request):
    """前端查询展示dashboard/BoxCard"""
    result = get_dashboard_BoxCard_handler()
    return DashboardResult(content=result)


@require_http_methods('dashboard/LineChart', methods=['POST'])
@signature(DashboardResult)
def dashboard_barChart(request):
    """前端查询展示dashboard/LineChart"""
    result = get_dashboard_barChart_handler()
    return DashboardResult(content=result)


@require_http_methods('dashboard/PieChart', methods=['POST'])
@signature(DashboardResult)
def dashboard_PieChart(request):
    """前端查询展示dashboard/PieChart"""
    result = get_dashboard_barChart_handler()
    return DashboardResult(content=result)


@require_http_methods('dashboard/RaddarChart', methods=['POST'])
@signature(DashboardResult)
def dashboard_RaddarChart(request):
    """前端查询展示dashboard/RaddarChart"""
    result = get_dashboard_barChart_handler()
    return DashboardResult(content=result)
