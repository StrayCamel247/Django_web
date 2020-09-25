from django.contrib.syndication.views import Feed
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from apps.accounts.models import Ouser
from apps.blog.models import Article, Category
#  Timeline
# from apps.tool.models import ToolLink
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, ArticleSerializer, CategorySerializer, PostHaystackSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .handler import IsAdminUserOrReadOnly
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.throttling import AnonRateThrottle

from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


import logging
logger=logging.getLogger('apps')
class APIResponse(Response):
    def __init__(self, data_status, data_msg, results=None,
                 status=None, headers=None, content_type=None, *args, **kwargs):
        data = {
            'code': data_status,
            'msg': data_msg
        }
        if results is not None:
            data['results'] = results

        data.update(kwargs)
        super().__init__(data=data, status=status,
                         headers=headers, content_type=content_type)


class MockResponse(Response):
    def __init__(self,  data,
                 status=None, headers=None, content_type=None, *args, **kwargs):
        super().__init__(data=data, status=status,
                         headers=headers, content_type=content_type)

from rest_framework.exceptions import APIException
class test_apiview(APIView):
    def get(self, req):
        a = 1/0
        # raise APIException('lalalalal')
        return APIResponse(200, "success", task_id="success", log_id="success", status=status.HTTP_200_OK)


class PostSearchAnonRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "5/min"}


class ArticleSearchView(HaystackViewSet):
    index_models = [Article]
    serializer_class = PostHaystackSerializer
    throttle_classes = [PostSearchAnonRateThrottle]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Ouser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class ArticleListSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryListSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# class TimelineListSet(viewsets.ModelViewSet):
#     queryset = Timeline.objects.all()
#     serializer_class = TimelineSerializer
#     permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


# class ToolLinkListSet(viewsets.ModelViewSet):
#     queryset = ToolLink.objects.all()
#     serializer_class = ToolLinkSerializer
#     permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class AllArticleRssFeed(Feed):
    # 显示在浏览器的标题
    title = 'Stray_Camel'
    # 跳转网址，为主页
    link = "/"
    # 描述内容
    description = 'Django个人博客类型网站'
    # 需要显示的内容条目，这个可以自己挑选一些热门或者最新的博客

    def items(self):
        return Article.objects.all()[:100]

    # 显示的内容的标题,这个才是最主要的东西
    def item_title(self, item):
        return "【{}】{}".format(item.category, item.title)

    # 显示的内容的描述
    def item_description(self, item):
        return item.body
