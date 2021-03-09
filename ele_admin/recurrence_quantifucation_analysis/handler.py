#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ :
# __REFERENCES__ :
# __date__: 2020/12/28 13
from typing import DefaultDict
from .models import Holding_Stock
from .tradingsystem import read_excel, make_excel, ParseQDII, JQ
import pandas as pd
from .constants import table_header
from django.contrib.sessions.models import Session
import datetime
from apps.api_exception import ParameterException


def _get_holding_stock(**params):
    """
    >>> df
    >>> {
        'code': {
            0: '000002', 1: '000338', 2: '000426', 3: '000533', 4: '000651', 5: '000786', 6: '000876', 7: '002191', 8: '002602', 9: '600009', 10: '600048', 11: '600380', 12: '600383', 13: '600585', 14: '600900', 15: '603719'
        },
        'cost': {
            0: 26.198, 1: 14.75, 2: 8.523, 3: 3.534, 4: 54.459, 5: 34.765, 6: 33.63, 7: 9.125, 8: 10.91, 9: 67.571, 10: 16.64, 11: 18.567, 12: 14.273, 13: 60.841, 14: 19.215, 15: 59.871
        },
        'num': {
            0: 200, 1: 500, 2: 300, 3: 1100, 4: 100, 5: 200, 6: 200, 7: 200, 8: 500, 9: 100, 10: 500, 11: 300, 12: 400, 13: 100, 14: 200, 15: 100
        }
    }
    """
    request = params.get('request')
    user_id = request.user.id
    limit, page = params['limit'], params['page']-1
    _filters = dict(
        user_id=user_id,
        is_deleted=False)
    if params['code']:
        _filters['code'] = params['code']
    stocks = Holding_Stock.objects.filter(**_filters).all()[
        page*limit:(page+1)*limit].values()
    df = pd.DataFrame(stocks)
    df['id'] = df.index
    return df


def del_holding_stock_handler(**params):
    """
    获取持仓数据
    """
    request = params.pop('request')
    user_id = request.user.id
    code = params.pop('code')
    params['is_deleted'] = True
    _ = Holding_Stock.objects.filter(
        user_id=user_id, code=code).update(**params)
    res = {
        'lines': _
    }
    return res


def put_holding_stock_handler(**params):
    """
    获取持仓数据
    """
    uni_colums = dict(
        user_id=params.get('request').user.id,
        is_deleted=False
    )
    day_date = datetime.datetime.now().strftime('%y-%m-%d-%h')
    params['day_date'] = day_date
    _params = rqa_market_stock_handler(**params)
    defaults = dict(
        **_params,
        num=params.pop('num'),
        cost=params.pop('cost')
    )
    _ = Holding_Stock.objects.update_or_create(**uni_colums, defaults=defaults)
    res = {
        'id': _[0].id,
        'is_new': _[-1]
    }
    return res


def get_holding_stock_handler(**params):
    """
    获取持仓数据
    """
    df = _get_holding_stock(**params)
    asceding, order_column = params.get(
        'sort')[:1] == '+', params.get('sort')[1:]
    if df.empty:
        res = {
            'items': [],
            'total': 0
        }
        return res
    if order_column not in df.columns:
        raise ParameterException(detail='排序字段不在数据中:%s' % order_column)
    df.sort_values(order_column,
                   ascending=[asceding], inplace=True)
    df = df.reset_index()
    df['id'] = df.index
    data = df.to_dict('records')
    res = {
        'items': data,
        'total': df.shape[0],
        'header': table_header
    }
    return res


def get_pred_stock_handler(**params):
    """
    获取股票收益情况
    """
    res = rqa_market_stock_handler(**params)

    return res


def rqa_market_stock_handler(**params):
    """
    股票量化分析-获取市场信息
    """
    df = _get_holding_stock(**params)
    # 构建dataframe 以数据库id为索引，删除用户id列
    sdk = JQ()
    df = read_excel(sdk, df)
    res = df.to_dict()
    return res
