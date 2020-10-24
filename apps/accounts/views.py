from apps.utils.core.http import require_http_methods
from apps.utils.wsme.signature import signature
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .handler import (token_obtain_pair_handler,
                      token_obtain_sliding_login_handler,
                      token_obtain_sliding_logout_handler,
                      token_refresh_handler, token_refresh_sliding_handler,
                      token_user_info_handler,
                      token_user_password_change_handler, token_verify_handler)
from .types import (AccountLoginBody, AccountPasswordChangeBody,
                    AccountRefreshBody, AccountsResult, AccountTokenBody)

# Create your views here.
urlpatterns = []


@require_http_methods('account/access_login', methods=['POST'])
@signature(AccountsResult, body=AccountLoginBody)
def token_obtain_pair(request, body):
    params = {
        'username': body.username,
        'password': body.password
    }
    content = token_obtain_pair_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/access_refresh', methods=['POST'])
@signature(AccountsResult, body=AccountRefreshBody)
def token_access_refresh(request, body):
    params = {
        'refresh': body.refresh
    }
    content = token_refresh_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token_login', methods=['POST'], jwt_required=False)
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


@require_http_methods('account/token_logout', methods=['POST'])
@signature(AccountsResult)
def token_obtain_sliding_logout(request):
    """用户登出"""
    params = dict(request=request)
    content = token_obtain_sliding_logout_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token_refresh', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_refresh(request, body):
    params = {
        'token': body.token
    }
    content = token_refresh_sliding_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token_verify', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_verify(request, body):
    params = {
        'token': body.token
    }
    content = token_verify_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/user_info', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_user_info(request, body):
    params = {
        'token': body.token
    }
    content = token_user_info_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/user_password_change', methods=['POST'])
@signature(AccountsResult, body=AccountPasswordChangeBody)
def token_user_password_change(request, body):
    params = {
        'id': body.id,
        'username': body.username,
    }
    content = token_user_password_change_handler(**params)
    return AccountsResult(content=content)
