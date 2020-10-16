#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : sql查询对象
# __REFERENCES__ : 
# __date__: 2020/10/16 21

import operator
import logging

import os
import psycopg2
import re
from psycopg2.extras import execute_values
from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import not_
from sqlalchemy import or_
from sqlalchemy import text
from sqlalchemy import cast
from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ColumnElement, _clause_element_as_expr

from apps.api_exception import DBError
from .base_db import db
from .complex_query import ValidatedComplexQuery
from django.conf import settings as conf

env = os.getenv('OPFF_ENV', 'dev')


LOG = logging.getLogger()


class Func(object):
    @staticmethod
    def _avg(field):
        return cast(func.avg(field), Float)

    @staticmethod
    def _sum(field):
        return cast(func.sum(field), String)


class Rollup(ColumnElement):
    def __init__(self, element):
        self.element = _clause_element_as_expr(element)


@compiles(Rollup)
def _mysql_rollup(element, compiler, **kw):
    return "%s WITH ROLLUP" % (compiler.process(element.element, **kw))


class QueryTransformer(object):
    operators = {"=": operator.eq,
                 "<": operator.lt,
                 ">": operator.gt,
                 "<=": operator.le,
                 "=<": operator.le,
                 ">=": operator.ge,
                 "=>": operator.ge,
                 "!=": operator.ne,
                 "in": lambda field_name, values: field_name.in_(values),
                 "=~": lambda field, value: field.op("regexp")(value)}

    # operators which are different for different dialects
    dialect_operators = {'postgresql': {'=~': (lambda field, value:
                                               field.op("~")(value))}}

    complex_operators = {"or": or_,
                         "and": and_,
                         "not": not_}
    aggr_operators = {"sum": Func._sum,
                      "count": func.count,
                      "max": func.max,
                      "min": func.min,
                      "avg": Func._avg}

    ordering_functions = {"asc": asc,
                          "desc": desc}

    def __init__(self, table, session_query, dialect='mysql'):
        self.session_query = session_query
        self.table = table
        self.query = None
        self.dialect_name = dialect
        self.allow_order_fields = None

    def set_query_field(self, aggr_expr, extend_model=False):
        if aggr_expr:
            groupby = aggr_expr.get("groupby", [])
            aggrs = aggr_expr.get("aggrs", [])

            self.allow_order_fields = [attr for attr in groupby]
            query_fields = [getattr(self.table, attr) for attr in groupby]
            for aggr in aggrs:
                fun_name, fields = list(aggr.items())[0]
                aggr_fun = self.aggr_operators[fun_name]
                for field in fields:
                    attr = getattr(self.table, field)
                    label_name = field + '_' + fun_name
                    query_fields.append(aggr_fun(attr).label(label_name))
                    self.allow_order_fields.append(label_name)
            self.query = self.session_query(*query_fields)
            return

        if extend_model:
            columns = [column for column in self.table.__table__.columns]
            self.query = self.session_query(*columns)
        else:
            self.query = self.session_query(self.table)

    def _get_operator(self, op):
        return (self.dialect_operators.get(self.dialect_name, {}).get(op)
                or self.operators[op])

    def _handle_complex_op(self, complex_op, nodes):
        op = self.complex_operators[complex_op]
        if op == not_:
            nodes = [nodes]
        element_list = []
        for node in nodes:
            element = self._transform(node)
            element_list.append(element)
        return op(*element_list)

    def _handle_simple_op(self, simple_op, nodes):
        op = self._get_operator(simple_op)
        field_name, value = list(nodes.items())[0]
        return op(getattr(self.table, field_name), value)

    def _transform(self, sub_tree):
        operator, nodes = list(sub_tree.items())[0]
        if operator in self.complex_operators:
            return self._handle_complex_op(operator, nodes)
        else:
            return self._handle_simple_op(operator, nodes)

    def apply_filter(self, expression_tree):
        condition = self._transform(expression_tree)
        self.query = self.query.filter(condition)

    def apply_options(self, orderby, limit, skip):
        self._apply_order_by(orderby)
        if limit is not None:
            self.query = self.query.limit(limit)
        if skip is not None:
            self.query = self.query.offset(skip)

    def _apply_order_by(self, orderby):
        if orderby is not None:
            for field in orderby:
                attr, order = list(field.items())[0]
                ordering_function = self.ordering_functions[order]
                if hasattr(self.table, attr):
                    self.query = self.query.order_by(ordering_function(
                        getattr(self.table, attr)))
                else:
                    self.query = self.query.order_by(ordering_function(attr))
        # elif hasattr(self.table, "create_time"):
        #     self.query = self.query.order_by(desc(self.table.create_time))

    def apply_aggr(self, aggr):
        groupby = None
        rollup = None
        # having = None

        if aggr is not None:
            groupby = aggr.get("groupby", [])
            rollup = aggr.get("rollup", False)
            # having = aggr.get("having", None)

        group_by = [getattr(self.table, attr) for attr in groupby]
        if rollup:
            self.query = self.query.group_by(Rollup(*group_by))
        else:
            self.query = self.query.group_by(*group_by)

    def get_query(self):
        return self.query


class DBUtil(object):

    @staticmethod
    def extend_query(db, db_model, filter_expr, orderby, skip, limit, aggr_expr=None, extend_model=False):

        bind = getattr(db_model, '__bind_key__', None)
        engine = db.get_engine(bind=bind)
        session = db.session
        session_query = session.query
        transformer = QueryTransformer(db_model, session_query,
                                       dialect=engine.dialect.name)
        transformer.set_query_field(aggr_expr, extend_model=extend_model)

        if filter_expr is not None:
            transformer.apply_filter(filter_expr)

        if aggr_expr is not None:
            transformer.apply_aggr(aggr_expr)

        total_query = transformer.get_query()

        transformer.apply_options(orderby,
                                  limit,
                                  skip)
        query = transformer.get_query()

        return query, total_query

    @staticmethod
    def get_extend_query(db, db_model, complex_query, extend_model=False):
        req_query = ValidatedComplexQuery(complex_query, db_model)
        req_query.validate()

        filter_expr = req_query.filter_expr
        orderby = req_query.orderby
        limit = req_query.limit
        skip = req_query.skip
        aggr_expr = req_query.aggr_expr
        query, total_query = DBUtil.extend_query(db, db_model, filter_expr,
                                                 orderby, skip, limit,
                                                 aggr_expr,
                                                 extend_model=extend_model)
        return query, total_query

    @staticmethod
    def query_format_data(db, db_model, complex_query):
        query, total_query = DBUtil.get_extend_query(db, db_model, complex_query,
                                                     extend_model=True)
        # count = total_query.count()

        datas = query.all()
        head = [x.get('name') for x in query.column_descriptions]
        format_data = map(lambda x: dict(zip(head, x)), datas)

        return format_data

    @staticmethod
    def query_flat_data(db, db_model, complex_query):
        query, total_query = DBUtil.get_extend_query(db, db_model, complex_query)
        # count = total_query.count()

        head = [x.get('name') for x in query.column_descriptions]
        data = query.all()
        return head, data

    @staticmethod
    def query_mode(db, db_model, complex_query):
        req_query = ValidatedComplexQuery(complex_query, db_model)
        req_query.validate()

        filter_expr = req_query.filter_expr
        orderby = req_query.orderby
        limit = req_query.limit
        skip = req_query.skip
        query, total_query = DBUtil.extend_query(db, db_model, filter_expr,
                                                 orderby, skip, limit)
        return query, total_query

    @staticmethod
    def fetch_data_sql(sql, params, bind_key=None):
        """
        :param sql: 查询sql
        :param params: 参数字典
        :param bind_key: 参数字
        :return: 查询结果
        """
        # con = session.connection()
        result = []
        render_sql(sql=sql, params=params)
        try:
            sql = text(sql)
            # con = con.execute(sql, params)
            con = db.session.execute(sql, params, bind=db.get_engine(current_app, bind=bind_key))
            if con.returns_rows:
                result = con.fetchall()
        except Exception as er:
            LOG.error("fetch data error: {0}, sql is: {1}".format(er, sql))
            raise DBError()
        else:
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
            sql = text(sql)
            # LOG.info(sql)
            # print(sql)
            # con = con.execute(sql, params)
            con = db.session.execute(sql, params, bind=db.get_engine(current_app, bind=bind_key))
            db.session.commit()
            lines = con.rowcount
        except Exception as er:
            print(er)
            LOG.error("update sql error: {0}, sql is: {1}".format(er, sql))
            db.session.rollback()
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
            sql = text(sql)
            LOG.info(sql)
            LOG.info(params_list)
            row_count_list = list(map(db.session.execute, repeat(sql), params_list))
            db.session.commit()
            lines = sum([res.rowcount for res in row_count_list])
        except Exception as er:
            print(er)
            LOG.error("update sql error: {0}, sql is: {1}".format(er, sql))
            db.session.rollback()
            raise DBError()
        else:
            return lines

    @staticmethod
    def execute_batch(sql=None, params_list=None, template=None):
        try:
            with psycopg2.connect(conf[env].SQLALCHEMY_DATABASE_URI) as conn:
                with conn.cursor() as cur:
                    execute_values(cur=cur, sql=sql, argslist=params_list, template=template)
                    row_count = cur.rowcount
                    # conn.commit()
        except Exception as er:
            LOG.error("execute_values error: {0}, sql is: {1}".format(er, sql))
            raise DBError()
        else:
            return row_count


def render_sql(sql=None, params=None):
    conn = psycopg2.connect(conf[env].SQLALCHEMY_DATABASE_URI)
    cur = conn.cursor()
    sql = re.sub('([^:]):(\w+)(?!:)', '\\1%(\\2)s', sql)
    try:
        logging.info(cur.mogrify(sql, params).decode('utf-8'))
    except Exception:
        pass
    cur.close()
    conn.close()
