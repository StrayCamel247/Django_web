#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 生成假数据
# __REFERENCES__ :
# __date__: 2020/10/22 14
import operator
import random
from datetime import datetime

from apps.constants import IsActiveConstant
from apps.utils.tools import ele_admin_chart_mapping
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.timezone import make_aware
from faker import Faker

User = get_user_model()

fake = Faker()


class KpiFactory:
    """kpi 指标工厂方法"""
    options = {
        "all_users"
    }

    @staticmethod
    def create_handler(_type):
        handler = dict(
            all_users=get_all_users_count_handler,
        )
        return handler[_type]


def kpi_online_user_via_all_handler(**params):
    pass


def kpi_indicator_handler(**params):
    request = params.get('request')
    res = ele_admin_chart_mapping(request)
    return res


def get_dashboard_BoxCard_handler(**params):
    """为BoxCard生成假数据"""
    res = dict(
        xAxis_data=['慕风', '纵浪', '帅', '清'],
        series_data=[[fake.random_int(min=20, max=2000)
                      for _ in range(5)] for name in range(5)],
        series_name=[fake.job() for _ in range(5)])

    return res


def get_dashboard_barChart_handler(**params):
    """为barChart生成假数据"""
    res = dict(
        xAxis_data=['慕风', '纵浪', '帅', '清'],
        series_data=[[fake.random_int(min=20, max=2000)
                      for _ in range(5)] for name in range(5)],
        series_name=[fake.job() for _ in range(5)])

    return res


def get_dashboard_LineChart_handler(**params):
    """为LineChart生成假数据"""
    res = dict(
        xAxis_data=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        lineChart_data=[
            dict(
                code=k, name=v, data=[fake.random_int(min=4000, max=30000) for _ in range(7)], normal=dict(color=n_c), areaStyle=dict(color=a_c), animationEasing=['quadraticOut', 'cubicInOut'][fake.random_int(min=0, max=1)])
            for k, v, n_c, a_c in zip(
                ['moofeng', 'zonglang', 'shuai', 'qing'], ['慕风', '纵浪', '帅', '清'], [
                    fake.hex_color() for _ in range(4)], [fake.hex_color() for _ in range(4)]
            )
        ]
    )
    return res


def get_dashboard_pieChart_handler(**params):
    """为pieChart生成假数据"""
    res = dict(
        linechart_data=sorted([
            dict(value=fake.random_int(min=80, max=300), name=v, code=k) for k, v in zip(['moofeng', 'zonglang', 'shuai', 'qing'], ['慕风', '纵浪', '帅', '清'])
        ], key=operator.itemgetter('value', 'code'), reverse=True)
    )
    return res


def get_dashboard_RaddarChart_handler(**params):
    """为RaddarChart生成假数据"""
    indicator_names = [fake.country() for _ in range(7)]
    data = [dict(value=dict(zip(indicator_names, [
        fake.random_int(min=10000, max=25000)
        for _ in range(7)])), name=n) for n in ['慕风', '纵浪', '帅', '清']
    ]
    res = dict(
        data=data,
        indicator=[dict(name=_, max=30000) for _ in indicator_names]
    )
    return res


def get_dashboard_TodoList_handler(**params):
    """为TodoList生成假数据"""
    res = [
        dict(
            text=fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None),
            done=[
                True, False][fake.random_int(min=0, max=1)]
        ) for _ in range(fake.random_int(min=6, max=10))
    ]
    return res


def get_all_users_count_handler(**params):
    """获得系统全部用户数量"""
    all_user_num = User.objects.filter(
        is_active=IsActiveConstant.ACTIVE).count()
    return all_user_num


def get_all_logged_in_users(**params):
    """获得在线用户"""
    # 获取没有过期的session
    print(settings.SESSION_ENGINE)
    sessions = Session.objects.filter(
        expire_date__gte=make_aware(datetime.now()))
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
    return "{}/{}".format(online_user_num, all_user_num)


def generate_transaction_list(**params):
    import uuid

    # 随机生成10个日期字符串
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
