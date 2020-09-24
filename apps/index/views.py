#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 12:40:21

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.views import generic
from django.contrib.sitemaps import Sitemap
from apps.blog.models import Article, Category
from django.db.models.aggregates import Count
from django.conf import settings
# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
# 分页
from markdown.extensions.toc import TocExtension
from pure_pagination.mixins import PaginationMixin

from apps.utils.wsme.signature import signature
from .types import HelloResult, HelloBody
from .handler import hello_handler
import json

class HelloView(generic.View):
    """测试get请求"""
    @signature(HelloResult, str, str)
    def get(self, brand, constraint):
        result = hello_handler()
        return HelloResult(content=result)
    
    @signature(HelloResult, ignore_extra_args=True)
    def post(self, request):
        # print(11111)
        # # body = json.loads(body.body)
        # params = {
        #     "test": body.test
        # }
        result = hello_handler()
        return HelloResult(content=result)
    




class MySearchView(SearchView):
    # 返回搜索结果集
    context_object_name = 'search_list'
    # 设置分页
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    # 搜索结果以浏览量排序
    queryset = SearchQuerySet().order_by('-views')


class IndexView(PaginationMixin, generic.ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(IndexView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'views':
            return ('-views')
        if sort == 'create_date':
            return ('-create_date')
        if sort == 'update_date':
            return ('-update_date')
        return ordering
# 文章聚类


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.update_date


# 分类聚类
class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

    def lastmod(self, obj):
        return obj.article_set.first().create_date

# 全局变量


def global_setting(request):
    return{
        "AUTHOR_NAME": settings.AUTHOR_NAME,
        "AUTHOR_DESC": settings.AUTHOR_DESC,
        "AUTHOR_EMAIL": settings.AUTHOR_EMAIL,
        "AUTHOR_TITLE": settings.AUTHOR_TITLE,
        "SITE_DESCRIPTION": settings.SITE_DESCRIPTION,
        "SITE_KEYWORDS": settings.SITE_KEYWORDS,
        "ONLINE_TIME_DAYS": settings.ONLINE_TIME_DAYS,
        "DOMAIN_NAME": 'http://'+request.get_host(),
    }


@login_required
@require_POST
def AddmessageView(request):
    if request.is_ajax():
        data = request.POST
        new_user = request.user
        new_content = data.get('content')
        rep_id = data.get('rep_id')
        if not rep_id:
            new_message = Message(author=new_user, content=new_content, parent=None,
                                  rep_to=None)
        else:
            new_rep_to = Message.objects.get(id=rep_id)
            new_parent = new_rep_to.parent if new_rep_to.parent else new_rep_to
            new_comment = Message(author=new_user, content=new_content, parent=new_parent,
                                  rep_to=new_rep_to)
        new_comment.save()
        new_point = '#com-' + str(new_comment.id)
        return JsonResponse({'msg': '留言提交成功！', 'new_point': new_point})
    return JsonResponse({'msg': '留言失败！'})


@require_POST
def mark_to_delete(request):
    '''将一个成员删除'''
    if request.is_ajax():
        data = request.POST
        contacts = request.user
        member = data.get('id')
        info = get_object_or_404(
            Notification, contacts_p=contacts, member_p=member)
        info.delete()
        return JsonResponse({'msg': 'delete success'})
    return JsonResponse({'msg': 'miss'})




