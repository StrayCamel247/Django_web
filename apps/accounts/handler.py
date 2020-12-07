#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 基于https://github.com/SimpleJWT/django-rest-framework-simplejwt 开发jwt-TOKEN验证脚手架
# __REFERENCES__ :
# __date__: 2020/10/10 14
import inspect
import logging
import re
from collections import OrderedDict
from datetime import date

import pandas as pd
import six
from apps.api_exception import InvalidJwtToken, InvalidUser
from apps.apis.serializers import UserSerializer
from apps.role.models import get_role_via_user
from apps.utils.core.session.handler import (_get_user_session_key,
                                             session_logout,
                                             session_user_update)
from apps.utils.wsme import json
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenObtainSlidingSerializer,
    TokenRefreshSerializer, TokenRefreshSlidingSerializer)

from .models import Ouser, UserInfoSerializer, get_page_via_user

log = logging.getLogger('apps')


def token_obtain_sliding_logout_handler(**params):
    """
    用户登出，更新用户信息，注销request信息等
    """
    try:
        current_request = params.get('request')
        assert params.get('request')
        session_logout(current_request)
    except Exception as e:
        log.warn(e)
        raise InvalidJwtToken(msg=six.text_type(e))
    return '登出成功'


def get_tree(df, index_key, parent_key):
    """

    :param df: pandas DataFrame
    :param index_key:
    :param parent_key:
    :return:
    """
    # drop掉 某行 index_key 和 parent_key 同时为null的数据; 替换nan为none
    result = df.dropna(how='all', subset=[index_key, parent_key]).where(df.notnull(), None)

    result["index"] = result[index_key]
    result.set_index("index", inplace=True)

    # 移除value为空的数据
    result = result[~(result[index_key].isnull())]
    # 记录转为字典，格式 {“index1”： row1_dict， “index2”：row2_dict ...}
    result_dict = result.to_dict(orient="index", into=OrderedDict)
    # 获取根节点列表
    # root_key = [i for i in result[result[parent_key].isna()].index]
    root_key = []
    for index, row in result_dict.items():
        if not row[parent_key] in result_dict:
            root_key.append(index)

    # 获取parent分组， 格式 {“parent1”： childrenes_list,  “parent2”： childrens_list}
    parent_groups = result.groupby(parent_key).groups
    for group, childrens in parent_groups.items():
        # 在result_dict上维护父子关系
        for children in childrens:
            if result_dict.get(group):
                result_dict[group].setdefault(
                    "children", []).append(result_dict[children])
            else:
                break
    content = []
    # 获取维护好父子关系result_dict中的根节点
    for i in root_key:
        content.append(result_dict[i])

    return content, result_dict


def token_obtain_sliding_login_handler(request, username: '用户名', password: '密码') -> dict:
    """
    Takes a set of user credentials and returns a sliding JSON web token to
    prove the authentication of those credentials.

    """
    ser = TokenObtainSlidingSerializer(
        data={get_username_field(): username, 'password': password})
    try:
        ser.is_valid(raise_exception=True)
    except:
        raise InvalidUser('用户名/密码输入错误')
    update_last_login(None, ser.user)
    session_user_update(request, ser.user)
   
    res = {
        'token': ser.validated_data.get('token')
    }
    return res


def token_user_password_change_handler(**kwrags):
    """用户根据id或者username+邮箱验证修改密码"""
    user_id = kwrags.get('id')
    res = dict(user=UserSerializer(user_id).data)
    # TODO:待开发
    pass


def get_username_field():
    try:
        username_field = Ouser.USERNAME_FIELD
    except AttributeError:
        username_field = 'username'

    return username_field


def token_user_info_handler(token):
    """
    date通过token获取user的基本信息
    用户序列化后的数据
    >>> user:{
        avatar: "/media/avatar/default/default%20(32).jpg"
        date_joined: "2020-12-03T12:35:09.587579+08:00"
        email: "aboyinsky@outlook.com"
        id: 1
        introduction: "沉默是金😂"
        is_active: true
        is_staff: true
        is_superuser: true
        last_login: "2020-12-04T13:19:59.311240+08:00"
        username: "admin"
        }
    >>> roles:['admin']
    通过用户信息获取所属角色的界面权限并返回/前端根据返回权限进行渲染
    """
    # 查询用户序列化信息
    _user = Ouser.query_user_from_token(token)
    res = {
        'user': UserInfoSerializer(_user).data
    }
    # 查询用户所属路由信息
    pages_data = get_page_via_user(user_id=_user.id)
    pages_df = pd.DataFrame(pages_data)
    pages, _ = get_tree(pages_df, 'page_id', 'parent_id')
    # 查询用户角色信息
    role = get_role_via_user(user_id=_user.id)
    roles = {
        'roles': [_[0] for _ in role],
        'pages':pages
    }
    res = dict(res, **roles)
    return res


def token_verify_handler(token):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    _user = Ouser.query_user_from_token(token)
    res = dict(user=UserSerializer(_user).data)
    return res


def token_refresh_sliding_handler(token):
    """
    采用滑动式JSON网络TOKEN，并在TOKEN的刷新期限尚未到期时返回新的刷新版本。
    """
    ser = TokenRefreshSlidingSerializer(data={'token': token})
    try:
        ser.is_valid(raise_exception=True)
    except AssertionError as e:
        log.info('token校验出错')
        raise InvalidJwtToken(detail='token校验出错')
    res = dict(token=ser.validated_data.get('token'))
    return res


def token_obtain_pair_handler(username, password):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    ser = TokenObtainPairSerializer(
        data={get_username_field(): username, 'password': password})
    ser.is_valid(raise_exception=True)
    update_last_login(None, ser.user)
    res = dict(refresh=ser.validated_data.get('refresh'),
               access=ser.validated_data.get('access'),
               user=UserSerializer(ser.user).data
               )
    return res


def token_refresh_handler(refresh):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    ser = TokenRefreshSerializer(data={'refresh': refresh})
    ser.is_valid(raise_exception=True)
    res = dict(refresh=ser.validated_data.get('refresh'),
               access=ser.validated_data.get('access')
               )
    return res
