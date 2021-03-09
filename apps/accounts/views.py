#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : *登陆接口化，继承rest framework框架登陆路由，扩展使用jwt原理扩展接口
# __REFERENCES__ :
# __date__: 2020/12/04 13
from django.contrib.auth import get_user_model
from apps.utils.core.http import require_http_methods
from apps.utils.wsme.signature import signature
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from .handler import (token_obtain_pair_handler,
                      token_obtain_sliding_login_handler,
                      token_obtain_sliding_logout_handler,
                      token_refresh_handler, token_refresh_sliding_handler,
                      token_user_info_handler,
                      token_user_info_change_handler, token_verify_handler)
from .types import (AccountLoginBody, AccountInfoChangeBody,
                    AccountRefreshBody, AccountsResult, AccountTokenBody, QueryUserInfo)

# Create your views here.
urlpatterns = []

User = get_user_model()


@require_http_methods('api/auth/get-users', methods=['POST'])
@signature(AccountsResult, body=QueryUserInfo)
def get_users(request, body):
    """
    模糊查询用户
    """
    users = User.get_users(body)
    content = {"users": users}
    return AccountsResult(msg=str(_('get users success')), content=content)


@require_http_methods('account/access-login', methods=['POST'])
@signature(AccountsResult, body=AccountLoginBody)
def token_obtain_pair(request, body):
    params = {
        'username': body.username,
        'password': body.password
    }
    content = token_obtain_pair_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/access-refresh', methods=['POST'])
@signature(AccountsResult, body=AccountRefreshBody)
def token_access_refresh(request, body):
    params = {
        'refresh': body.refresh
    }
    content = token_refresh_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token-login', methods=['POST'], jwt_required=False)
@signature(AccountsResult, body=AccountLoginBody)
def token_obtain_sliding_login(request, body):
    """用户登陆"""
    params = {
        'request': request,
        'username': body.username,
        'password': body.password
    }
    content = token_obtain_sliding_login_handler(
        **params)
    return AccountsResult(content=content)


@require_http_methods('account/token-logout', methods=['POST'])
@signature(AccountsResult)
def token_obtain_sliding_logout(request):
    """用户登出"""
    params = dict(request=request)
    content = token_obtain_sliding_logout_handler(**params)
    return AccountsResult(content=content)

# 用户状态刷新


@require_http_methods('account/token-refresh', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_refresh(request, body):
    params = {
        'token': body.token
    }
    content = token_refresh_sliding_handler(**params)
    return AccountsResult(content=content)

# 用户信息验证


@require_http_methods('account/token-verify', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_verify(request, body):
    params = {
        'token': body.token
    }
    content = token_verify_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/user-info', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_user_info(request, body):
    params = {
        'token': body.token
    }
    content = token_user_info_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/user-info-modify', methods=['PUT'])
@signature(AccountsResult, body=AccountInfoChangeBody)
def token_user_info_modify(request, body):
    """
    用户密码修改-基础信息修改
    """
    params = {
        'request': request,
        'password': body.password,
    }
    content = token_user_info_change_handler(**params)
    return AccountsResult(content=content)
