#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 11:09:55


import socket
def get_host_ip():
    """查询本机ip地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_local_host_ip(params=None):
    """获取本机"""
    # 太网适配器 IPV4:
    ip = socket.gethostbyname(socket.gethostname())
    # 局域网 IPV4
    if not ip:
        ip = get_host_ip()
    return ip
