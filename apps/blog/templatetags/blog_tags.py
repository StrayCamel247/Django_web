
# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import Article,FriendLink, Category,  Keyword
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
import re

# 注册自定义标签函数
register = template.Library()


# 获取导航条大分类查询集
@register.simple_tag
def get_categoty_list():
    """返回大分类列表"""
    return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)


# 返回文章分类查询集



# 获取归档文章查询集
@register.simple_tag
def get_data_date():
    """获取文章发表的不同月份"""
    article_dates = Article.objects.datetimes('create_date', 'month', order='DESC')
    return article_dates


@register.simple_tag
def keywords_to_str(art):
    '''将文章关键词变成字符串'''
    keys = art.keywords.all()
    return ','.join([key.name for key in keys])


# 返回活跃的友情链接查询集
@register.simple_tag
def get_friends():
    """获取活跃的友情链接"""
    return FriendLink.objects.filter(is_show=True, is_active=True)




# 获取热门排行数据查询集，参数：sort 文章类型， num 数量
@register.simple_tag
def get_article_list(sort=None, num=None):
    """获取指定排序方式和指定数量的文章"""
    if sort:
        if num:
            return Article.objects.order_by(sort)[:num]
        return Article.objects.order_by(sort)
    if num:
        return Article.objects.all()[:num]
    return Article.objects.all()


@register.simple_tag
def get_article_num():
    """获取指定排序方式和指定数量的文章"""

    return Article.objects.all().count()

# 返回文章列表模板
#inclusion_tag里面的内容用下面函数的返回值渲染，然后作为一个组件一样，加载到使用这个函数的html文件里面
@register.inclusion_tag('index.html')
def load_article_summary(articles):
    """返回文章列表模板"""
    return {'articles': articles}



# 返回分页信息
@register.inclusion_tag('blog/tags/pagecut.html', takes_context=True)
def load_pages(context):
    """分页标签模板，不需要传递参数，直接继承参数"""
    return context


@register.simple_tag
def get_request_param(request, param, default=None):
    """获取请求的参数"""
    return request.POST.get(param) or request.GET.get(param, default)


# 获取前一篇文章，参数当前文章 ID
@register.simple_tag
def get_article_previous(article_id):
    has_previous = False
    id_previous = int(article_id)
    while not has_previous and id_previous >= 1:
        article_previous = Article.objects.filter(id=id_previous - 1).first()
        if not article_previous:
            id_previous -= 1
        else:
            has_previous = True
    if has_previous:
        article = Article.objects.filter(id=id_previous).first()
        return article
    else:
        return


# 获取下一篇文章，参数当前文章 ID
@register.simple_tag
def get_article_next(article_id):
    has_next = False
    id_next = int(article_id)
    article_id_max = Article.objects.all().order_by('-id').first()
    id_max = article_id_max.id
    while not has_next and id_next <= id_max:
        article_next = Article.objects.filter(id=id_next + 1).first()
        if not article_next:
            id_next += 1
        else:
            has_next = True
    if has_next:
        article = Article.objects.filter(id=id_next).first()
        return article
    else:
        return



# 获取文章 keywords
@register.simple_tag
def get_article_keywords(article):
    keywords = []
    keys = Keyword.objects.filter(article=article)
    for key in keys:
        keywords.append(key.name)
    return ','.join(keywords)

#搜索高亮
@register.simple_tag
def my_highlight(text, q):
    """自定义标题搜索词高亮函数，忽略大小写"""
    if len(q) > 1:
        try:
            text = re.sub(q, lambda a: '<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text

