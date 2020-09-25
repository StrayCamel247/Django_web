# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from .views import (md_html ,default_upload, admin_upload
                    )
# from .views import (md_html, Toolview, BD_pushview, bd_api_view, BD_pushview_site, bd_api_site, Link_testview,
#                     Link_test_api, regexview, regex_api, useragent_view, useragent_api, html_characters, mdeditor_upload,
#                     )
app_name = "tool"

from django.urls import path
urlpatterns = [
    # 工具汇总页
    url(r'^default_upload/$', default_upload.as_view(), name='default_uploads'),
    url(r'^admin_upload/$', admin_upload.as_view(), name='admin_upload'),
]
