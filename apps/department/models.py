#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 用户部门管理等
# __REFERENCES__ :
# __date__: 2020/09/28 09
from django.db import models
from django.conf import settings
from datetime import datetime


class Department(models.Model):
    class Meta:
        verbose_name = """部门信息管理"""
        verbose_name_plural = verbose_name
        db_table = "department_message"
    parent_department = models.IntegerField(
        verbose_name=u"父类部门id", null=True, blank=True)
    name = models.CharField(max_length=20, verbose_name=u"部门名称", default="")
    manager = models.IntegerField(verbose_name=u"部门经理", null=True, blank=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    class Meta:
        verbose_name = """员工信息管理"""
        verbose_name_plural = verbose_name
        db_table = "staff_message"
    department = models.IntegerField(verbose_name="部门", null=True, blank=True)
    name = models.CharField(max_length=20, verbose_name=u"员工姓名")
    email = models.EmailField(
        default='straycamel@straycamel.com', verbose_name=u"邮箱")
    gradSchool = models.CharField(max_length=20, verbose_name=u"毕业学校")
    address = models.CharField(max_length=50, verbose_name=u"住址", default='2')
    sex = models.CharField(max_length=10, choices=(
        ('female', u'女'), ('male', u'男')), verbose_name=u"性别")
    age = models.IntegerField(verbose_name=u"年龄")
    birthday = models.DateField(verbose_name=u"生日")
    tel = models.CharField(max_length=20, verbose_name=u"手机号")
    salary_num = models.IntegerField(default=0, verbose_name=u"薪资")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"入职时间")
    user = models.IntegerField(blank=True, null=False)
    is_activate = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
