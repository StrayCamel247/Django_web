#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 11:09:55

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import time
import os
import re
import requests

import sys
import logging
import datetime


class ImageStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        # 重新文件上传
        import hashlib
        # 获取文件后缀
        ext = '.bmp'
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件夹名称
        fn = time.strftime(
            '%Y%m%d%H%M%S')
        fn = hashlib.md5(time.strftime(
            '%Y%m%d%H%M%S').encode('utf-8')).hexdigest()
        name = os.path.join(d, fn+ext)
        # 调用父类方法
        return super(ImageStorage, self)._save(name, content)


# 打印时间的装饰器
def logging_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        print("this function <", func.__name__, ">is running")
        res = func(*args, **kwargs)
        print("this function <", func.__name__,
              "> takes time：", datetime.datetime.now()-start)
        return res
    return wrapper
