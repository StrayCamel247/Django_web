from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.user.models import Ouser
from apps.blog.models import Article, Category, Timeline
from apps.tool.models import ToolLink, ToolCategory


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


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(read_only=True)
    keywords = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Article
        # fields = ('id', 'author', 'title', 'views', 'category', 'tags')
        # fields = '__all__'
        exclude = ('body',)


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'



class ToolCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolCategory
        fields = '__all__'

        
class ToolLinkSerializer(serializers.ModelSerializer):
    category = ToolCategorySerializer()
    class Meta:
        model = ToolLink
        fields = '__all__'