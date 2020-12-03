#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : ele_admin管理系统配置数据库
# __REFERENCES__ :
# __date__: 2020/12/03 15
from datetime import datetime

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class ChartMapping(models.Model):
    """
    NOTE:
    base.ChartMapping.chart_body: (fields.W904) django.contrib.postgres.fields.JSONField is deprecated. Support for it (except in historical migrations) will be removed in Django 4.0.
        HINT: Use django.db.models.JSONField instead.

    """
    class Meta:
        verbose_name = """图标信息表头"""
        verbose_name_plural = verbose_name
        db_table = "ele_admin_chart_mapping"
    module_code = models.CharField(max_length=200, default="")
    url_code = models.CharField(max_length=200, default="")
    chart_body = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
