# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (md_html, Toolview, BD_pushview, bd_api_view, BD_pushview_site, bd_api_site, Link_testview,
                    Link_test_api, regexview, regex_api, useragent_view, useragent_api, html_characters, default_upload, admin_upload, game, snake, minesweeper,
                    )
# from .views import (md_html, Toolview, BD_pushview, bd_api_view, BD_pushview_site, bd_api_site, Link_testview,
#                     Link_test_api, regexview, regex_api, useragent_view, useragent_api, html_characters, mdeditor_upload,
#                     )
app_name = "tool"

from django.urls import path
urlpatterns = [
    # 工具汇总页
    url(r'^$', Toolview, name='total'),
    # 在线编辑
    url(r'^md2html/$', md_html, name='md2html'),
    # url(r'^mdeditor_upload/$', mdeditor_upload.as_view(), name='mdeditor_upload'),
    url(r'^default_upload/$', default_upload.as_view(), name='default_uploads'),
    url(r'^admin_upload/$', admin_upload.as_view(), name='admin_upload'),
    # 百度主动推送
    url(r'^baidu-linksubmit/$', BD_pushview, name='baidu_push'),
    # 百度推送ajax
    url(r'^baidu-linksubmit/ajax/$', bd_api_view, name='baidu_push_api'),
    # 百度主动推送sitemap
    url(r'^baidu-linksubmit-for-sitemap/$',
        BD_pushview_site, name='baidu_push_site'),
    url(r'^baidu-linksubmit-for-sitemap/ajax/$',
        bd_api_site, name='baidu_push_api_site'),
    # 友链检测
    url(r'^link-test/$', Link_testview, name='link_test'),
    url(r'^link-test/ajax/$', Link_test_api, name='link_test_api'),
    # 正则表达式在线
    url(r'^regex/$', regexview, name='regex'),
    url(r'^regex/ajax/$', regex_api, name='regex_api'),
    # user-agent生成器
    url(r'^user-agent/$', useragent_view, name='useragent'),
    url(r'^user-agent/ajax/$', useragent_api, name='useragent_api'),
    # HTML特殊字符查询
    url(r'^html-special-characters/$', html_characters, name='html_characters'),
    # 游戏世界
    url(r'^game/$', game, name='game'),
    url(r'^game/Snake/$', snake, name='snake'),
    url(r'^game/Minesweeper/$', minesweeper, name='minesweeper'),
]
