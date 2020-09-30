#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : apis视图定义
# __REFERENCES__ : 
# __date__: 2020/09/30 09
from django.contrib.syndication.views import Feed
from django.http import request
from django.shortcuts import render

from django.contrib.auth.models import User, Group
from apps.accounts.models import Ouser
from apps.blog.models import Article, Category
from apps.department.models import Department
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, ArticleSerializer, CategorySerializer, PostHaystackSerializer, DepartmentSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .handler import IsAdminUserOrReadOnly
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.throttling import AnonRateThrottle

from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
import logging
logger = logging.getLogger('apps')


class DepartmentViewSet(ModelViewSet):
    """
    API endpoint that allows Departments to be viewed or edited.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class APIResponse(Response):
    def __init__(self, data_status, data_msg, results=None,
                 status=None, headers=None, content_type=None, *args, **kwargs):
        data = {
            'status_code': data_status,
            'detail': data_msg
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

# @serializer_signature(, body)


class test_apiview(APIView):
    def get(self, request):
        a = 1/0
        # raise APIException('lalalalal')
        return APIResponse(200, "success", task_id="success", log_id="success", status=status.HTTP_200_OK)


# import json
# @serializer_signature(testresult, body=testbody)
# def test(body):
def test(requests):
    print(requests)
    print(1)
    res = testresult(dict(code='1234', mesage='1234'))
    print(res.data)
    # print(request)
    # print(request.GET)
    # ser = testbody(data=json.loads(request.body))
    # # ser.is_valid(raise_exception=True)#返回TRUE,表示校验成功，否则没有校验成
    # # a = 1/0
    # print(ser.initial_data)
    # # print(ser._kw)
    # res = testresult(dict(code='1234', mesage='1234'))
    # print(res.data)
    # return HttpResponse(json.dumps(res.data), content_type='application/json')


class PostSearchAnonRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "5/min"}


class ArticleSearchView(HaystackViewSet):
    index_models = [Article]
    serializer_class = PostHaystackSerializer
    throttle_classes = [PostSearchAnonRateThrottle]


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Ouser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Ouser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class ArticleListSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryListSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# class TimelineListSet(ModelViewSet):
#     queryset = Timeline.objects.all()
#     serializer_class = TimelineSerializer
#     permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


# class ToolLinkListSet(ModelViewSet):
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
