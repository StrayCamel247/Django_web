from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from apps.utils.core.http import require_http_methods
from apps.utils.wsme.signature import signature
from .types import AccountsResult, AccountLoginBody, AccountTokenBody, AccountRefreshBody, AccountPasswordChangeBody
from .handler import token_refresh_sliding_handler, token_obtain_sliding_login_handler, token_obtain_sliding_logout_handler, token_refresh_handler, token_obtain_pair_handler, token_verify_handler, token_user_info_handler, token_user_password_change_handler
# Create your views here.
urlpatterns = []


@require_http_methods('account/access_login', methods=['POST'])
@signature(AccountsResult, body=AccountLoginBody)
def token_obtain_pair(body):
    params = {
        'username': body.username,
        'password': body.password
    }
    content = token_obtain_pair_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/access_refresh', methods=['POST'])
@signature(AccountsResult, body=AccountRefreshBody)
def token_access_refresh(body):
    params = {
        'refresh': body.refresh
    }
    content = token_refresh_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token_login', methods=['POST'], ini_request=True)
@signature(AccountsResult, body=AccountLoginBody)
def token_obtain_sliding_login(body):
    """用户登陆"""
    params = {
        'username': body.username,
        'password': body.password
    }
    content = token_obtain_sliding_login_handler(
        **params)
    return AccountsResult(content=content)


@require_http_methods('account/token_logout', methods=['GET'], jwt_required=True)
@signature(AccountsResult)
def token_obtain_sliding_logout():
    """用户登出"""
    content = token_obtain_sliding_logout_handler()
    return AccountsResult(content=content)


@require_http_methods('account/token_refresh', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_refresh(body):
    params = {
        'token': body.token
    }
    content = token_refresh_sliding_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token_verify', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_verify(body):
    params = {
        'token': body.token
    }
    content = token_verify_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/user_info', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_user_info(body):
    params = {
        'token': body.token
    }
    content = token_user_info_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/user_password_change', methods=['POST'], jwt_required=True)
@signature(AccountsResult, body=AccountPasswordChangeBody)
def token_user_password_change(body):
    params = {
        'id': body.id,
        'username': body.username,
    }
    content = token_user_password_change_handler(**params)
    return AccountsResult(content=content)
