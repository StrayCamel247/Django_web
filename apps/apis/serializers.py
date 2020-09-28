from drf_haystack.serializers import HaystackSerializerMixin
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.accounts.models import Ouser
from apps.blog.models import Article, Category, Timeline
from apps.role.models import Department
# from apps.tool.models import ToolLink, ToolCategory
class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ouser
        fields = ['id', 'username', 'email',
                  'is_staff', 'is_active', 'date_joined']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


# https://www.zmrenwu.com/courses/django-rest-framework-tutorial/materials/101/


class PostHaystackSerializer(HaystackSerializerMixin, ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        search_fields = ["key_word"]


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'


# class ToolCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ToolCategory
#         fields = '__all__'


# class ToolLinkSerializer(serializers.ModelSerializer):
#     category = ToolCategorySerializer()
#     class Meta:
#         model = ToolLink
#         fields = '__all__'
