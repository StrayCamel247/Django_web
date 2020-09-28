#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : restful framework 框架的使用
# __REFERENCES__ : 参考官方文档和https://www.zmrenwu.com/courses/django-rest-framework-tutorial/materials/101/
# __date__: 2020/09/28 12
from drf_haystack.serializers import HaystackSerializerMixin
from django.contrib.auth.models import User, Group
from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
from apps.accounts.models import Ouser
from apps.blog.models import Article, Category, Timeline
from apps.department.models import Department
# from apps.tool.models import ToolLink, ToolCategory
class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Ouser
        fields = ['id', 'username', 'email',
                  'is_staff', 'is_active', 'date_joined']


class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


class PostHaystackSerializer(HaystackSerializerMixin, ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        search_fields = ["key_word"]


class TimelineSerializer(ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'


# class ToolCategorySerializer(ModelSerializer):
#     class Meta:
#         model = ToolCategory
#         fields = '__all__'


# class ToolLinkSerializer(ModelSerializer):
#     category = ToolCategorySerializer()
#     class Meta:
#         model = ToolLink
#         fields = '__all__'
