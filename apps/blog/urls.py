from django.conf.urls import url
from .views import IndexView, DetailView, CategoryView, MySearchView, TimelineView
app_name='blog'
urlpatterns = [
    # 首页，自然排序
    url(r'^$', IndexView.as_view(template_name='index.html'), name='index'),  
    # 文章详情页面
    url(r'^article/(?P<slug>.*?)/$', DetailView.as_view(), name='article'),
    # 主页，按照浏览量排序
    url(r'^hot/$', IndexView.as_view(), {'sort': 'v'}, name='index_hot'),  
    # 给我留言
    # url(r'^category/message/$', MessageView, name='message'),
    # 关于自己
    # url(r'^category/about/$', AboutView, name='about'),
    # 赞助作者
    # url(r'^category/donate/$', DonateView, name='donate'),
    # 技术交流
    # url(r'^category/exchange/$', ExchangeView, name='exchange'),
    # 项目合作
    # url(r'^category/project/$', ProjectView, name='project'),
    # 提问交流
    # url(r'^category/question/$', QuestionView, name='question'),
    # 全文搜索
    url(r'^search/$', MySearchView.as_view(), name='search'),
    # 分类页面
    url(r'^category/(?P<slug>[\w-]+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<slug>[\w-]+)/hot/$', CategoryView.as_view(), {'sort': 'v'},
        name='category_hot'),
    # 归档页面
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/$', IndexView.as_view(template_name='archive.html'), name='date'),
    # timeline页面
    url(r'^timeline/$', TimelineView.as_view(), name='timeline'),  
]
