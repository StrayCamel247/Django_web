#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/25 11:37:04
from rest_framework import permissions
from django.urls.resolvers import URLResolver, URLPattern
from django.utils.module_loading import import_string
from collections import OrderedDict
from django.conf import settings


def recursion_urls(pre_namespace: '以后用户拼接name', pre_url: '以后用于拼接url', urlpatterns: '路由关系列表', url_ordered_dict: '用于保存递归中获取的所有路由'):
    """递归的去获取URL"""
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发
            if not item.name:
                continue
            if pre_namespace:
                name = '%s:%s' % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + str(item.pattern)

            url_ordered_dict[name] = {
                'name': name, 'url': url.replace('^', '').replace('$', '')}
        elif isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = '%s:%s' % (pre_namespace, item.namespace)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + str(item.pattern),
                           item.url_patterns, url_ordered_dict)


def get_all_url_dict(*args, **kwargs):
    """获取项目中所有的URL"""
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归去获取所有的路由
    return url_ordered_dict


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
