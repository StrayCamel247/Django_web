
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, ArticleListSet, CategoryListSet, TimelineListSet, ToolLinkListSet, AllArticleRssFeed
from django.conf.urls import include
from apps.index.views import HelloView
router = routers.DefaultRouter()
router.register(r'all_users', UserViewSet)
router.register(r'user_groups', GroupViewSet)
router.register(r'all_categorys', CategoryListSet)
router.register(r'all_articles', ArticleListSet)
router.register(r'timelines', TimelineListSet)
router.register(r'all_tools', ToolLinkListSet)

# rest_framework框架
urlpatterns = [
    path('rest_framework/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# rss订阅
urlpatterns += [
    url(r'rss/$', AllArticleRssFeed(), name='rss'),
]

# 自定义api
urlpatterns += [
    path('hello', HelloView.as_view()),
]

