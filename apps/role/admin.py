#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 部门角色管理
# __REFERENCES__ : 
# __date__: 2020/09/28 08
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Department,Staff


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('parent_department','name','manager')

@admin.register(Staff)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','department','gradSchool','tel','add_time')
