#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 用户部门管理等
# __REFERENCES__ :
# __date__: 2020/09/28 09
from django.db import models


class role(models.Model):
    class Meta:
        verbose_name = """角色信息"""
        verbose_name_plural = verbose_name
        db_table = "role"

    def __str__(self):
        return self.name
    # 角色id
    role_id = models.IntegerField(
        verbose_name=u"父类部门id", primary_key = True)
    # 角色名称
    role_name = models.CharField(max_length=20, verbose_name=u"部门名称", default="浪子",unique=True)
    create_date = models.DateTimeField(verbose_name='创建时间')
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
