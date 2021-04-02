#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 项目启动配置基础文件
# __REFERENCES__ :
# __date__: 2020/12/03 12
import os


def setdefault_django_settings_module():
    """
    项目启动前若不适用默认文件，则需要配置此环境变量
    >>> import os
    >>> os.environ['django_web_flag'] = 'dev'
    >>> env = os.getenv('django_web_flag', 'loc')
    """
    env = os.getenv('django_web_flag', 'loc')
    # 设置django默认环境变量 DJANGO_SETTINGS_MODULE
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          'config.{}_settings'.format(env))
