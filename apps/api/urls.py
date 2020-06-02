
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, ArticleListSet, CategoryListSet, TimelineListSet, ToolLinkListSet, AllArticleRssFeed
from django.conf.urls import include
router = routers.DefaultRouter()
router.register(r'all_users', UserViewSet)
router.register(r'user_groups', GroupViewSet)
router.register(r'all_categorys', CategoryListSet)
router.register(r'all_articles', ArticleListSet)
router.register(r'timelines', TimelineListSet)
router.register(r'all_tools', ToolLinkListSet)

urlpatterns = [
    # rest_framework
    path('v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # rss订阅
    url(r'rss/$', AllArticleRssFeed(), name='rss'),
]