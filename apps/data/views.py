#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 获取模型需要训练的数据集，只获取不修改，构建redis/pickle缓存系统，尽可能自动下载数据集并缓存。  
# __REFERENCES__ : 
# __date__: 2020/09/27 16

from apps.utils.wsme.signature import signature
from apps.utils.core.http import require_http_methods
from .types import DataResultResult