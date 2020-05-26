#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 12:40:21

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
        if sort == 'v':
            return ('-views', '-update_date', '-id')
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
    }
