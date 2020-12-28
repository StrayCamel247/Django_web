#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 获取模型需要训练的数据集，只获取不修改，构建redis/pickle缓存系统，尽可能自动下载数据集并缓存。
# __REFERENCES__ :
# __date__: 2020/09/27 16

import re


from apps.utils.wsme.signature import signature
from apps.utils.core.http import require_http_methods
from .types import RQAResult
from .handler import get_holding_stock_handler
# url锚点，让config.urls中集合url的机制可以访问到，并调用require_http_methods将url注册到apis中，和restful接口相集合
urlpatterns = []


@require_http_methods('rqa/holding-stock', methods=['GET'])
@signature(RQAResult, int, int, str)
def get_holding_stock(request, page, limit, sort):
    """用户持仓数据查询"""
    params = dict(
        page=page, limit=limit, sort=sort,
        request=request,
    )
    result = get_holding_stock_handler(**params)
    return RQAResult(content=result)
