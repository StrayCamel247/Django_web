from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.accounts.models import Ouser
from apps.blog.models import Article, Category, Timeline
# from apps.tool.models import ToolLink, ToolCategory


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
    # author_id = serializers.ReadOnlyField(source='author.username')
    # category_id = CategorySerializer(read_only=True)
    # keywords = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='name'
    # )

    class Meta:
        model = Article
        # fields = ('id', 'author_id', 'title', 'views', 'category_id', 'tags','body')
        fields = '__all__'
        # exclude = ('body',)

# https://www.zmrenwu.com/courses/django-rest-framework-tutorial/materials/101/
from drf_haystack.serializers import HaystackSerializerMixin

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