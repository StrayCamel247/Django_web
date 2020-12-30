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
        unique_together = (("code",  "user_id"),)
    code = models.CharField(max_length=200, default="")
    cost = models.FloatField(max_length=200, default=0.00)
    num = models.FloatField(max_length=200, default=0.00)
    user_id = models.CharField(max_length=200, null=True)
    is_deleted = models.BooleanField(
        verbose_name='已删除', default=False, null=True)