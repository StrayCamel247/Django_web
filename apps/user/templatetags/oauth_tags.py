# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import Ouser

register = template.Library()

@register.simple_tag
def get_user_avatar_tag(user):
    '''返回用户的头像，是一个img标签'''
    img = user.avatar
    return img

    
