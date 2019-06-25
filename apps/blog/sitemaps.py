# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import Article, Category, Tag
from django.db.models.aggregates import Count


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
