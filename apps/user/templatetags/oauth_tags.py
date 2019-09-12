# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import Ouser,Contacts
from django.db.models.aggregates import Count
register = template.Library()

@register.simple_tag
def get_user_avatar_tag(user):
    '''返回用户的头像，是一个img标签'''
    return {'user':user}


@register.simple_tag
def get_contacts_list():
    '''返回标签列表'''
    return Contacts.objects.annotate(total_num=Count('ouser')).filter(total_num__gt=0)


@register.simple_tag
def get_users_list():
    '''返回全部用户字典'''
    return Ouser.objects.all()

@register.simple_tag
def get_users_num():
    '''返回全部用户的数量'''
    return Ouser.objects.count()

@register.simple_tag
def get_users_bynameid(the_name,the_id):
    '''按照昵称和id获取用户'''
    return Ouser.objects.filter(username=the_name,id=the_id)