#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 数据校验
# __REFERENCES__ : 
# __date__: 2020/10/14 11
from apps.api_exception import ParameterException
import six


def Percentile_check(field_value):
    from decimal import Decimal
    try:
        assert len(str(Decimal(field_value).quantize(Decimal('0.00')))) >= len(
            field_value), '两位小数检查，field_value：{field_value}'.format(field_value=field_value)
    except Exception as e:
        raise ParameterException(six.text_type(e))


def date_check(field_value):
    """日期字符串检查，要求的格式：2019-01-01"""
    try:
        datetime.datetime.strptime(field_value, "%Y-%m-%d")
    except Exception as e:
        error_msg = '日期检查，field_value：{field_value}'
        # Logger.info(error_msg.format(field_value=field_value))
        raise ParameterException(_(error_msg.format(field_value=field_value)))


def int_check(field_value):
    """int字符串检查"""
    try:
        int(field_value)
    except Exception as e:
        error_msg = 'int字符串检查，field_value：{field_value}'
        # Logger.info(error_msg.format(field_value=field_value))
        raise ParameterException(_(error_msg.format(field_value=field_value)))
