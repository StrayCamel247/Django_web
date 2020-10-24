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
config = {
    'dev':'config.dev_settings',
    'loc':'config.loc_settings'
}
def execute_from_command_line(argv=None):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", config['loc'])
    utility = LocalManagement(argv)
    utility.execute()


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
