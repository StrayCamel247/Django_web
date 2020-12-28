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
    from django.core.paginator import Paginator, Page  # 导入模块
    stock_list = Holding_Stock.objects.filter(
        user_id=user_id).all()
    paginator = Paginator(stock_list, 10)
    # 创建一个对象paginator，又有这是一个对象，所以可以通过点“.”来调用一些功能
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象
    stocks = paginator.page(number=1).object_list
    print(stocks)
    df = pd.DataFrame(stocks)
    return df


def get_holding_stock_handler(**params):
    """
    获取持仓数据
    """
    df = _get_holding_stock(**params).drop('user_id', axis=1)
    res = {
        'items': df.to_dict('records'),
        'total': df.shape[0]
    }
    return res


def rqa_pred_stock_handler(**params):
    df = _get_holding_stock(**params)
    # 构建dataframe 以数据库id为索引，删除用户id列
    df = df.set_index('id').drop('user_id', axis=1)
    sdk = JQ()
    df = read_excel(sdk, df)
    make_excel(df)
    print(df)
    print(df.to_dict())
    s = ParseQDII()
    pre_stock_data = s.get_stock_data()
    return pre_stock_data
