#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : django 启动文件
# __REFERENCES__ :
# __date__: 2020/10/10 17
from apps.utils.management import LocalManagement
from django.conf import settings
import os
import sys


def setdefault_django_settings_module():
    """
    项目启动前若不适用默认文件，则需要配置此环境变量
    >>> import os
    >>> os.environ['django_web_flag'] = 'dev'

    
    >>> env = os.get('django_web_env', 'loc')
    """
    env = os.get('django_web_env', 'loc')
    # 设置django默认环境变量 DJANGO_SETTINGS_MODULE
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          'config.{}_settings'.format(env))


def execute_from_command_line(argv=None):
    setdefault_django_settings_module()
    utility = LocalManagement(argv)
    utility.execute()


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
