#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 用户部门管理等
# __REFERENCES__ :
# __date__: 2020/09/28 09
from apps import system_name
from apps.utils.django_db import DBUtil
from django.db import models


class Role(models.Model):
    class Meta:
        verbose_name = """角色信息"""
        verbose_name_plural = verbose_name
        db_table = "{sys}_role".format(sys=system_name)

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
    is_deleted = models.BooleanField(verbose_name='已删除', default=False, null=True)


class RolePagePermission(models.Model):
    class Meta:
        verbose_name = """角色页面权限关系表"""
        verbose_name_plural = verbose_name
        db_table = "{sys}_role_page_permission".format(sys=system_name)

    def __str__(self):
        return self.name
    operation_type = models.IntegerField(
        verbose_name=u"0无权限、1有权限", default=0)
    role_id = models.IntegerField(
        verbose_name=u"用户")
    page_id = models.IntegerField(
        verbose_name=u"界面路由")


def get_role_via_user(**params):
    """根据用户id获取用户角色"""
    from apps.accounts.models import User_role
    params = dict({
        'user_role_tablename': User_role._meta.db_table,
        'role_tablename': Role._meta.db_table
    }, **params)
    sql = """
        SELECT
            role_name
        FROM
            {role_tablename} 
        WHERE
            role_id IN ( SELECT role_id FROM {user_role_tablename} WHERE user_id =:user_id )
        order by weight desc
    """.format(**params)
    result = DBUtil.fetch_data_sql(sql, params=params)
    return result
