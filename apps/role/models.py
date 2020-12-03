#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 用户部门管理等
# __REFERENCES__ :
# __date__: 2020/09/28 09
from django.db import models

from apps.utils.django_db import DBUtil


class Role(models.Model):
    class Meta:
        verbose_name = """角色信息"""
        verbose_name_plural = verbose_name
        db_table = "role"

    def __str__(self):
        return self.name
    # 角色id
    role_id = models.IntegerField(
        verbose_name=u"父类部门id", primary_key=True)
    # 角色名称
    role_name = models.CharField(
        max_length=20, verbose_name=u"部门名称", default="", unique=True)
    weight = models.IntegerField(
        verbose_name=u"角色权重", default=0)
    create_date = models.DateTimeField(verbose_name='创建时间')
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)


class PagePermission(models.Model):
    class Meta:
        verbose_name = """页面权限表"""
        verbose_name_plural = verbose_name
        db_table = "page_permission"
    # 页面id
    page_id = models.IntegerField(verbose_name=u"页面id", primary_key=True)
    # 页面名称
    page_name = models.CharField(
        max_length=20, verbose_name=u"页面名称", default="", unique=True)
    # 页面路由
    page_route = models.CharField(
        max_length=150, verbose_name=u"页面路由", default="", unique=True)
    # 页面上一级页面id
    parent_id = models.IntegerField(
        verbose_name=u"页面上一级页面id")
    # 页面的权重
    weight = models.IntegerField(verbose_name=u"页面的权重")
    # 图标
    icon = models.CharField(
        max_length=20, verbose_name=u"图标", default="", unique=True)


# 根据用户id获取用户角色
def get_role_via_user(params={}):
    from apps.accounts.models import User_role
    params = dict({'user_role': User_role._meta.model_name,
                   'role': Role._meta.model_name}, **params)
    sql = """
        SELECT
            role_name
        FROM
            {role} 
        WHERE
            role_id IN ( SELECT role_id FROM {user_role} WHERE user_id =:user_id )
        order by weight desc
    """.format(**params)
    result = DBUtil.fetch_data_sql(sql, params=params)
    return result
