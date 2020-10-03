#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 获取模型需要训练的数据集，只获取不修改，构建redis/pickle缓存系统，尽可能自动下载数据集并缓存。  
# __REFERENCES__ : 
# __date__: 2020/09/27 16

from apps.utils.wsme.signature import signature
from apps.utils.core.http import require_http_methods
from .types import DataResult,DataResultBody
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .handler import get_iris_data
# url锚点，让config.urls中集合url的机制可以访问到，并调用require_http_methods将url注册到apis中，和restful接口相集合
urlpatterns=[]
@require_http_methods('data/iris_data', methods=['GET'])
@signature(DataResult, int)
def iris_data_view(page):
    data = get_iris_data(page=page)
    res = DataResult(content=data)
    return res
