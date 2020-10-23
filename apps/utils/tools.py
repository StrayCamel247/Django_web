#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ :
# __REFERENCES__ :
# __date__: 2020/10/23 09
from apps.utils.django_db import DBUtil
from apps.utils.core.http import REQUEST
#   TODO 开发时注释掉缓存
# @cache.cached(timeout=1000, key_prefix='charts_map/%s')


def chart_mapping():
    sql = """
        select chart_body
        from chart_mapping
        WHERE url_code=:url_code
    """
    path = REQUEST.path
    result = DBUtil.fetch_data_sql(sql=sql, params={"url_code": path})
    result, = result[0]
    return result
