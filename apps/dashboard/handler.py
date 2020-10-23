#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 生成假数据
# __REFERENCES__ :
# __date__: 2020/10/22 14
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.constants import IsActiveConstant
from apps.utils.tools import chart_mapping
User = get_user_model()

class KpiFactory:
    """kpi 指标工厂方法"""
    options = {
        "online_user_via_all"
    }

    @staticmethod
    def create_handler(_type):
        handler = dict(
            online_user_via_all=get_all_logged_in_users,
        )
        return handler[_type]


def kpi_online_user_via_all_handler(**params):
    pass

def kpi_indicator_handler():
    res = chart_mapping()
    return res
def get_all_logged_in_users(**params):
    """获得在线用户"""
    # 获取没有过期的session
    print(settings.SESSION_ENGINE)
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    uid_list = []

    # 获取session中的userid
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # 根据userid查询user
    online_user_num = User.objects.filter(
        id__in=uid_list, is_active=IsActiveConstant.ACTIVE).count()
    all_user_num = User.objects.filter(
        is_active=IsActiveConstant.ACTIVE).count()
    return "{}/{}".join(online_user_num/all_user_num)


def generate_transaction_list(**params):
    import uuid
    # 随机生成10个日期字符串
    from faker import Faker
    fake = Faker()
    data = [dict(update_time=fake.date_time_this_year(before_now=True,  after_now=False,
                                                      tzinfo=None).strftime('%Y-%m-%d %H:%M:%S'), order_no=str(uuid.uuid1()), username=fake.name(),
                 status=['sucess', 'pedding'][random.randint(0, 1)],
                 price=random.randint(1000, 2000)
                 ) for _ in range(25)]
    per_page, page = params.get('per_page', 10), params.get('page', 11)
    paginator = Paginator(data, per_page)
    try:
        contacts = paginator.page(page)
    except EmptyPage:
        page = 1
        contacts = paginator.page(paginator.num_pages)
    all_pages = contacts.paginator.num_pages
    data_length = contacts.paginator.count
    res = dict(
        total=data_length,
        items=contacts.object_list,
        all_pages=all_pages,
        per_page=per_page,
        page=page,
    )
    return res
