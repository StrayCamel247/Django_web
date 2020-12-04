#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : ele_admin管理系统配置数据库
# __REFERENCES__ :
# __date__: 2020/12/03 15
from datetime import datetime

from django.conf import settings
# from django.contrib.postgres.fields import JSONField
from django.db import models
from ele_admin import system_name


class PagePermission(models.Model):
    class Meta:
        verbose_name = """eleadmin页面权限表"""
        verbose_name_plural = verbose_name
        db_table = "{sys}_page_permission".format(sys=system_name)
    # 页面id
    page_id = models.IntegerField(verbose_name=u"页面id", primary_key=True)
    # 页面名称
    page_name = models.CharField(
        max_length=20, verbose_name=u"页面名称", default="")
    # 页面路径
    page_path = models.CharField(
        max_length=150, verbose_name=u"页面路径", null=True)
    # 页面路由
    page_route = models.CharField(
        max_length=150, verbose_name=u"页面路由", null=True)
    # 页面上一级页面id
    parent_id = models.IntegerField(
        verbose_name=u"页面上一级页面id", null=True)
    # 页面的权重
    weight = models.IntegerField(verbose_name=u"页面的权重", null=True)
    # 图标
    icon = models.CharField(
        max_length=20, verbose_name=u"图标", default="")
    # 评论
    remark = models.CharField(
        max_length=200, verbose_name=u"评论", null=True)
    
    is_deleted = models.BooleanField(verbose_name='已删除', default=False, null=True)

class ChartMapping(models.Model):
    """
    NOTE:
    base.ChartMapping.chart_body: (fields.W904) django.contrib.postgres.fields.JSONField is deprecated. Support for it (except in historical migrations) will be removed in Django 4.0.
        HINT: Use django.db.models.JSONField instead.

    """
    class Meta:
        verbose_name = """图标信息表头"""
        verbose_name_plural = verbose_name
        db_table = "{sys}_chart_mapping".format(sys=system_name)
    module_code = models.CharField(max_length=200, default="")
    url_code = models.CharField(max_length=200, default="")
    chart_body = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
