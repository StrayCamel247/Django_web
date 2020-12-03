#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : django 启动文件
# __REFERENCES__ :
# __date__: 2020/10/10 17
import sys

from django.conf import settings

from apps.utils.management import LocalManagement
from config.handler import setdefault_django_settings_module


def execute_from_command_line(argv=None):
    """
    通过命令行启动项目
    >>> python manage.py runserver 
    or
    >>> python manage.py runserver 0.0.0.0:8000 --noreload
    """
    setdefault_django_settings_module()
    utility = LocalManagement(argv)
    utility.execute()


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
