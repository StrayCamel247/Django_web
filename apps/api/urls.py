
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, ArticleListSet, CategoryListSet, TimelineListSet, ToolLinkListSet

router = routers.DefaultRouter()
router.register(r'all_users', UserViewSet)
router.register(r'user_groups', GroupViewSet)
router.register(r'all_categorys', CategoryListSet)
router.register(r'all_articles', ArticleListSet)
router.register(r'timelines', TimelineListSet)
router.register(r'all_tools', ToolLinkListSet)
