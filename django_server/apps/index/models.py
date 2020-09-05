from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from mdeditor.fields import MDTextField
from django.http import HttpResponse
from uuslug import slugify
from django.utils.text import slugify as sfy
from django_blog.settings import MEDIA_ROOT
import markdown
from markdown.extensions.toc import TocExtension
import emoji, re, time, string, os
from apps.utils.handler import ImageStorage


# slider_right_table
# class SliderRightTable(models.model):
#     order = models.IntegerField(verbose_name='排序', null=False, default='1')
#     card_name = models.CharField('卡片名称', max_length=50)

# 友情链接表
class FriendLink(models.Model):
    name = models.CharField('网站名称', max_length=50)
    description = models.CharField('网站描述', max_length=100, blank=True)
    link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址')
    logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否有效', default=True)
    is_show = models.BooleanField('是否首页展示', default=False)
    is_deleted = models.BooleanField('是否已删除', default=False)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

    def get_home_url(self):
        """提取友链的主页"""
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active=False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])

