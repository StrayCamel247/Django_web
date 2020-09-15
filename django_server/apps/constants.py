#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 常量文件
# __date__: 2020/09/15 16

import os
from concurrent.futures import (ALL_COMPLETED, ThreadPoolExecutor,
                                as_completed, wait)
import multiprocessing
# 获取系统最大多线程数

MAX_CPUS = multiprocessing.cpu_count()//(1-0.9)