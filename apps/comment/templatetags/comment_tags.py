# 创建了新的tags标签文件后必须重启服务器

from django import template
from django.utils import timezone
from ..models import Message
register = template.Library()

@register.simple_tag
def recall_com(mes):
    """判断message创建日期是否为一天前"""
    time = timezone.localtime(timezone.now())
    return max((time - mes.create_date).days, 1)
    
@register.simple_tag
def get_comment_count(entry):
    '''获取一个文章的评论总数'''
    lis = entry.article_comments.all()
    return lis.count()

@register.simple_tag
def get_parent_comments(entry):
    '''获取一个文章的父评论列表'''
    lis = entry.article_comments.filter(parent=None)
    return lis

@register.simple_tag
def get_child_comments(com):
    '''获取一个父评论的子平路列表'''
    lis = com.articlecomment_child_comments.all()
    return lis

@register.simple_tag
def get_comment_user_count(entry):
    '''获取评论人总数'''
    p = []
    lis = entry.article_comments.all()
    for each in lis:
        if each.author not in p:
            p.append(each.author)
    return len(p)

@register.simple_tag
def get_notifications(user,f=None):
    '''获取一个用户的对应条件下的提示信息'''
    if f=='true':
        lis = user.notification_get.filter(is_read=True)
    elif f=='false':
        lis = user.notification_get.filter(is_read=False)
    else:
        lis = user.notification_get.all()
    return lis

@register.simple_tag
def get_notifications_count(user,f=None):   
    '''获取一个用户的对应条件下的提示信息总数'''
    if f=='true':
        lis = user.notification_get.filter(is_read=True)
    elif f=='false':
        lis = user.notification_get.filter(is_read=False)
    else:
        lis = user.notification_get.all()
    return lis.count()


# 留言板
@register.simple_tag
def get_message_num():
    """获取网站留言的总数"""
    return Message.objects.all().count()

@register.simple_tag
def get_message_date():
    """获取不同月份留言"""
    message_dates = Message.objects.datetimes('create_date', 'month', order='DESC')
    return article_dates

@register.simple_tag
def get_parent_message():
    '''父留言列表'''
    lis = Message.objects.filter(parent=None)
    return lis

@register.simple_tag
def get_child_messages(com):
    '''获取一个父留言的子平路列表'''
    lis = com.child_messages.all()
    return lis

@register.simple_tag
def get_message_user_count(entry):
    '''获取留言人总数'''
    p = []
    lis = Message.objects.all()
    for each in lis:
        if each.author not in p:
            p.append(each.author)
    return len(p)