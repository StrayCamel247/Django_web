"""
JWT 的数据结构:
它是一个很长的字符串，中间用点（.）分隔成三个部分。注意，JWT 内部是没有换行的，这里只是为了便于展示，将它写成了几行。
xxxxxxxxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyy.zzzzzzzzzzzzzzzzzzzzzzzz
JWT 的三个部分依次如下。

Header（头部）
Payload（负载）
Signature（签名）

写成一行，就是下面的样子。
Header.Payload.Signature
"""
import jwt

from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .settings import api_settings


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class BaseJSONWebTokenAuthentication(BaseAuthentication):
    """
    基于jwt的token验证
    此认证方案使用[HTTP](https://tools.ietf.org/html/rfc2617) 基本认证，针对用户的用户名和密码进行认证。基本认证通常只适用于测试。
    如果认证成功 BasicAuthentication 提供以下信息。
    request.user 将是一个 Django User 实例。
    request.auth 将是 None。
    那些被拒绝的未经身份验证的请求会返回使用适当WWW-Authenticate标头的HTTP 401 Unauthorized响应。例如：
    """

    def authenticate(self, request):
        """
        校验输入，如果用户不存在返回None，如果存在则返回数据
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, payload)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """
    JWT系统认证
    通过http请求头中的"Authorization"中传递的密钥进行身份验证
    """
    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):
        """获取JWT的值"""
        # 获取http请求头中HTTP_AUTHORIZATION
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        # 如果没有HTTP_AUTHORIZATION
        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        # 如果HTTP_AUTHORIZATION和JWT头部分不匹配
        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        # 如果HTTP_AUTHORIZATION长度为
        if len(auth) == 1:
            msg = _('无效请求头')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)
