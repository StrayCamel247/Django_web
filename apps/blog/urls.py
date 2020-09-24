from django.conf.urls import url
from .views import DetailView, CategoryView, TimelineView
app_name = 'blog'
urlpatterns = [
    # 文章详情页面
    url(r'^article/(?P<slug>.*?)/$', DetailView.as_view(), name='article'),
    # 分类页面
    url(r'^category/(?P<slug>[\w-]+)/$',
        CategoryView.as_view(), name='category'),
    url(r'^category/(?P<slug>[\w-]+)/hot/$', CategoryView.as_view(), {'sort': 'v'},
        name='category_hot'),
    # timeline页面
    url(r'^timeline/$', TimelineView.as_view(), name='timeline'),
]
