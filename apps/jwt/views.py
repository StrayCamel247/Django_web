from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from apps.utils.core.http import require_http_methods
from apps.utils.wsme.signature import signature
from .types import JWTResult,JWTLoginBody
from .settings import api_settings
from .serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)
# url锚点，让config.urls中集合url的机制可以访问到，并调用require_http_methods将url注册到apis中，和restful接口相集合
urlpatterns=[]
# jwt_response_payload_handler = api_settings.jwt_response_payload_handler
from .handler import jwt_response_payload_handler
@require_http_methods('account/login', methods=['POST'])
@signature(JWTResult,body=JWTLoginBody)
def jwt_token_login(body):
    """结合jwt校验token的方式进行登陆"""
    pass

class JSONWebTokenAPIView(APIView):
    """
    基于APIView的JWTapi视图
    """
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        """
        提供给serializer class的额外上下文。
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        返回用于serializer的类。
        Defaults to using `self.serializer_class`.
        支持定制化获取不同的信息：
        例如：管理员获得完整的序列化，其他获得基本的序列化
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        返回serializer instance应该用于validating and
        deserializing input, and for serializing output。
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 将输入的数据序列化
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,token,expires=expiration,httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    接收带有用户名和密码的POST的API View。
    返回可用于已认证请求的JSON Web令牌。
    """
    serializer_class = JSONWebTokenSerializer


class VerifyJSONWebToken(JSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = VerifyJSONWebTokenSerializer


class RefreshJSONWebToken(JSONWebTokenAPIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    serializer_class = RefreshJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()
