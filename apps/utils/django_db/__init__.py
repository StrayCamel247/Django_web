#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : sql查询对象
# __REFERENCES__ :
# __date__: 2020/10/16 21

from apps.types import ListType
import operator
import logging

import os
import re
from typing import Dict, List, Tuple

from apps.api_exception import DBError
from django.conf import settings as conf
from django.db import connection as conn
from django.db.transaction import rollback, commit


LOG = logging.getLogger('apps')


class DBUtil(object):
    @staticmethod
    def fetch_data(sql, params):
        """根据sql/params查询数据，返回字段信息和数据"""
        sql = render_sql(sql=sql, params=params)
        try:
            cur = conn.cursor()
            con = cur.execute(sql, params)
            res = dict(data=cur.fetchall())
            # 将获取的数据和查询的字段组为dict
            description = [
                col[0] if col else 'unknown' for col in cur.description]
            res['description'] = description
            cur.close()
            return res
        except Exception as er:
            LOG.error("fetch data error: {0}, sql is: {1}".format(er, sql))
            raise DBError()

    @staticmethod
    def fetch_data_sql(sql, params):
        """仅返回获取的数据"""
        res = DBUtil.fetch_data(sql, params)
        return res.get('data')

    @staticmethod
    def fetch_data_dict_sql(sql, params) -> Dict:
        """返沪{字段:[格式]}"""
        res = DBUtil.fetch_data(sql, params)
        result = {dec: [_[k] for _ in res.get(
            'data')] for k, dec in enumerate(res.get('description'))}
        return result

    @staticmethod
    def fetch_data_list_sql(sql, params) -> List:
        """返沪[{字段:_} for _ in 数据]格式"""
        res = DBUtil.fetch_data(sql, params)
        result = [dict(zip([col[0] for col in res.get('description')], row))
                  for row in res.get('data')]
        return result

    @staticmethod
    def update_data_sql(sql, params, bind_key=None):
        """
        :param sql:
        :param params:
        :param bind_key:
        :return:
        """
        # con = session.connection()
        render_sql(sql=sql, params=params)
        try:
            cur = conn.cursor()
            con = cur.execute(sql, params)
            lines = con.rowcount
        except Exception as er:
            print(er)
            LOG.error("update sql error: {0}, sql is: {1}".format(er, sql))
            rollback()
            raise DBError()
        else:
            return lines

    @staticmethod
    def batch_update_sql(sql, params_list):
        """ Newest SQLAlchemy can use batch mode such as psycopg2`s execute_batch() function ,
        But it`s only supported for insert, not update

        :param sql:
        :param params_list:
        # :param bind_key:
        :return:
        """
        from itertools import repeat
        try:

            cur = conn.cursor()
            row_count_list = list(
                map(cur.execute, repeat(sql), params_list))
            commit()
            lines = sum([res.rowcount for res in row_count_list])
        except Exception as er:
            LOG.error("update sql error: {0}, sql is: {1}".format(er, sql))
            rollback()
            raise DBError()
        else:
            return lines


def render_sql(sql=None, params=None):
    """
    SQL = 'SELECT * FROM brokers WHERE broker_name LIKE %(broker_name)s AND broker_id > %(broker_id)s'
    test = dict(
        broker_name='A%',
        broker_id=10
    )

    print(SQL % test)


    """
    cur = conn.cursor()
    # 自定义输入格式
    sql = re.sub('([^:]):(\w+)(?!:)', '\\1%(\\2)s', sql)
    # try:
    logging.info(sql % params)
    # except Exception:
    #     logging.warn('sql日志打印失败')
    cur.close()
    return sql
