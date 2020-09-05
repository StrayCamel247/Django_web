"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
import os
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.contrib import admin

# 网站地图
from django.contrib.sitemaps.views import sitemap
from apps.index.views import ArticleSitemap, CategorySitemap
# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap
}

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # Django-mdeditor URLS
    path('mdeditor/', include('mdeditor.urls')),
    # index
    # path('', include('apps.blog.urls'), name='blog'),
    # path('', include('apps.index.urls'), name='index'),
    # 用户
    path('accounts/', include('allauth.urls'), name='accounts'),
    # path('accounts/', include('apps.accounts.urls'), name='accounts'),
    # 评论
    # path('comment/', include('apps.comment.urls'), name='comment'),
    # 网站地图
    # path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
    #      name='django.contrib.sitemaps.views.sitemap'),
    # re_path(r'^static/(?P<path>.*)$', serve,
    #         {'document_root': settings.STATIC_ROOT}),
    # rest_framework
    # path('api/', include('apps.api.urls'), name='api'),
    # tool
    # path('tool/', include('apps.tool.urls'), name='tool'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path(_+'/', include('apps.{app_name}.urls'.format(app_name=_)), name=_) for _ in settings.APPS if os.path.exists(os.path.join(settings.APPS_FLODER, _, 'urls.py'))]