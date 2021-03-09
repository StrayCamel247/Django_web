#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ :
# __REFERENCES__ :
# __date__: 2020/12/22 18
# from django.contrib.postgres.fields import JSONField
from django.db import models
from ele_admin import system_name

from apps.utils.django_db import DBUtil


class Holding_Stock(models.Model):
    """
    NOTE:
    base.ChartMapping.chart_body: (fields.W904) django.contrib.postgres.fields.JSONField is deprecated. Support for it (except in historical migrations) will be removed in Django 4.0.
        HINT: Use django.db.models.JSONField instead.
    """
    class Meta:
        verbose_name = """股票持仓"""
        verbose_name_plural = verbose_name
        db_table = "{sys}_holding_stock".format(sys=system_name)
        unique_together = (("code",  "user_id", "day_date"),)
    code = models.CharField(max_length=200, verbose_name="编号", null=True)
    name = models.CharField(max_length=200, verbose_name="名称", null=True)
    cost = models.FloatField(max_length=200, verbose_name="成本", null=True)
    num = models.FloatField(max_length=200, verbose_name="股数", null=True)
    trade = models.FloatField(max_length=200, verbose_name="现价", null=True)
    value = models.FloatField(max_length=200, verbose_name="市值", null=True)
    profit = models.CharField(max_length=200, verbose_name="盈亏", null=True)
    rise = models.CharField(max_length=200, verbose_name="涨幅", null=True)
    position = models.CharField(max_length=200, verbose_name="仓位", null=True)
    industry = models.CharField(max_length=200, verbose_name="行业", null=True)
    pe_ratio = models.FloatField(
        max_length=200, verbose_name="市盈率", null=True)
    pb_ratio = models.FloatField(
        max_length=200, verbose_name="市净率", null=True)
    ps_ratio = models.FloatField(
        max_length=200, verbose_name="市销率", null=True)
    pcf_ratio = models.CharField(
        max_length=200, verbose_name="市现率", null=True)
    day_date = models.CharField(
        max_length=200, verbose_name="数据日期", null=True)
    user_id = models.CharField(max_length=200, null=True)
    is_deleted = models.BooleanField(
        verbose_name='已删除', default=False, null=True)
