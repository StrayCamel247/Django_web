#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/09/04 16

from django.utils.translation import ugettext as _
from .models import Article
from apps.api_exception import Fail
def get_posts_handler(params=None):
    all_res = Article.objects.filter(is_deleted=False).all()
    if not all_res:
        raise Fail(msg=_('查不到数据'))
    return all_res