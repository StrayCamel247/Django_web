#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : apis视图定义
# __REFERENCES__ :
# __date__: 2020/09/30 09
import logging
from apps.utils.wsme.signature import signature
from apps.utils.core.http import require_http_methods
from .handler import get_all_url_dict
from .types import ApisResult
logger = logging.getLogger('apps')
from django.utils.translation import ugettext as _

# url锚点，让config.urls中集合url的机制可以访问到，并调用require_http_methods将url注册到apis中，和restful接口相集合
urlpatterns = []

@require_http_methods('all_urls', methods=['GET'])
@signature(ApisResult)
def get_all_url_dict_view():
    """获取项目中所有的URL"""
    content = get_all_url_dict()
    return ApisResult(content=content)
