from django.contrib.syndication.views import Feed
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from apps.user.models import Ouser
from apps.blog.models import Article, Category, Timeline
from apps.tool.models import ToolLink
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, ArticleSerializer, CategorySerializer, TimelineSerializer, ToolLinkSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .handler import IsAdminUserOrReadOnly


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


class TimelineListSet(viewsets.ModelViewSet):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class ToolLinkListSet(viewsets.ModelViewSet):
    queryset = ToolLink.objects.all()
    serializer_class = ToolLinkSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


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
