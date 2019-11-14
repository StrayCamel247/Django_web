# import markdown
import time
from django.views import generic
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import render, HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, Category, Tag, Timeline
# from markdown.extensions.toc import TocExtension  # 锚点的拓展
from django.core.cache import cache
from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet


# Create your views here.
class TimelineView(generic.ListView):
    model = Timeline
    template_name = 'timeline.html'
    context_object_name = 'timeline_list'

# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    # 返回搜索结果集
    context_object_name = 'search_list'
    # 设置分页
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    # 搜索结果以浏览量排序
    queryset = SearchQuerySet().order_by('-views')

class IndexView(generic.ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(IndexView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

  
class DetailView(generic.DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super(DetailView, self).get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        # if u != obj.author:
        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 10:
                    obj.update_views()
                    ses[the_key] = time.time()
        obj.update_views()
        ses[the_key] = time.time()
        # 文章可以使用markdown书写，带格式的文章，像csdn写markdown文章一样
        # md = markdown.Markdown(extensions=[
        #     'markdown.extensions.extra',
        #     'markdown.extensions.codehilite',
        #     TocExtension(slugify=slugify),
        # ])
        # obj.body = md.convert(obj.body)
        # obj.toc = md.toc
        return obj

class CategoryView(generic.ListView):
    model = Article
    template_name = 'category.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(CategoryView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(CategoryView, self).get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    def get_context_data(self, **kwargs):
        context_data = super(CategoryView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章分类'
        context_data['search_instance'] = cate
        return context_data


def global_setting(request):
    return{
        "AUTHOR_NAME" : settings.AUTHOR_NAME,
        "AUTHOR_DESC" : settings.AUTHOR_DESC,
        "AUTHOR_EMAIL" : settings.AUTHOR_EMAIL,
        "AUTHOR_TITLE" : settings.AUTHOR_TITLE,
        "SITE_DESCRIPTION" : settings.SITE_DESCRIPTION,
        "SITE_KEYWORDS" : settings.SITE_KEYWORDS,
    }



