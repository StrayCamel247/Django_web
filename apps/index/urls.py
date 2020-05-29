from django.conf.urls import url
from .views import IndexView, MySearchView
app_name = 'index'
urlpatterns = [
    # 首页，自然排序
    url(r'^$', IndexView.as_view(template_name='index.html'), name='index'),
    # 主页，按照编写排序
    url(r'^u/$', IndexView.as_view(), {'sort': 'update_date'}, name='index_hot'),
    # 主页，按照编写排序
    url(r'^c/$', IndexView.as_view(), {'sort': 'create_date'}, name='index_hot'),
    # 主页，按照浏览量排序
    url(r'^h/$', IndexView.as_view(), {'sort': 'views'}, name='index_hot'),
    # 归档页面
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/$',
        IndexView.as_view(template_name='archive.html'), name='date'),
    # 全文搜索
    url(r'^search/$', MySearchView.as_view(), name='search'),
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
]
