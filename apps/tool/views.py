#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/05/26 17:20:42

from django.views import generic
from mdeditor.configs import DEFAULT_CONFIG, MDConfig
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.html import mark_safe
from .apis.bd_push import push_urls, get_urls
from .apis.links_test import Check
from .apis.useragent import get_user_agent
import os
import re
import markdown
import datetime
import json
from mdeditor.views import UploadView

def Toolview(request):
    return render(request, 'tool/tool.html')
def game(request):
    return render(request, "tool/game/game_dir.html")


def snake(request):
    return render(request, "tool/game/snake.html")


def street_fighter(request):
    return render(request, "tool/game/StreetFighter.html")


def minesweeper(request):
    return render(request, "tool/game/Minesweeper.html")
    
# 在线md编辑


def md_html(request):
    return render(request, 'tool/md2html.html')


# 百度主动推送
def BD_pushview(request):
    return render(request, 'tool/bd_push.html')


@require_POST
def bd_api_view(request):
    if request.is_ajax():
        data = request.POST
        url = data.get('url')
        urls = data.get('url_list')
        info = push_urls(url, urls)
        return JsonResponse({'msg': info})
    return JsonResponse({'msg': 'miss'})


# 百度主动推送升级版，提取sitemap链接推送
def BD_pushview_site(request):
    return render(request, 'tool/bd_push_site.html')


@require_POST
def bd_api_site(request):
    if request.is_ajax():
        data = request.POST
        url = data.get('url')
        map_url = data.get('map_url')
        urls = get_urls(map_url)
        if urls == 'miss':
            info = "{'error':404,'message':'sitemap地址请求超时，请检查链接地址！'}"
        elif urls == '':
            info = "{'error':400,'message':'sitemap页面没有提取到有效链接，sitemap格式不规范。'}"
        else:
            info = push_urls(url, urls)
        return JsonResponse({'msg': info})
    return JsonResponse({'msg': 'miss'})


# 友链检测
def Link_testview(request):
    return render(request, 'tool/link_test.html')


@require_POST
def Link_test_api(request):
    if request.is_ajax():
        data = request.POST
        p = data.get('p')
        urls = data.get('urls')
        c = Check(urls, p)
        info = c.run()
        return JsonResponse(info)
    return JsonResponse({'msg': 'miss'})


# 在线正则表达式
def regexview(request):
    return render(request, 'tool/regex.html')


@require_POST
def regex_api(request):
    if request.is_ajax():
        data = request.POST
        texts = data.get('texts')
        regex = data.get('r')
        try:
            lis = re.findall(r'{}'.format(regex), texts)
        except:
            lis = []
        num = len(lis)
        info = '\n'.join(lis)
        result = "匹配到&nbsp;{}&nbsp;个结果：\n".format(
            num) + "```\n" + info + "\n```"
        result = markdown.markdown(result, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        return JsonResponse({'result': mark_safe(result), 'num': num})
    return JsonResponse({'msg': 'miss'})


# 生成请求头
def useragent_view(request):
    return render(request, 'tool/useragent.html')


@require_POST
def useragent_api(request):
    if request.is_ajax():
        data = request.POST
        d_lis = data.get('d_lis')
        os_lis = data.get('os_lis')
        n_lis = data.get('n_lis')
        d = d_lis.split(',') if len(d_lis) > 0 else None
        os = os_lis.split(',') if len(os_lis) > 0 else None
        n = n_lis.split(',') if len(n_lis) > 0 else None
        result = get_user_agent(os=os, navigator=n, device_type=d)
        return JsonResponse({'result': result})
    return JsonResponse({'msg': 'miss'})


# HTML特殊字符对照表
def html_characters(request):
    return render(request, 'tool/characters.html')


# TODO 此处获取default配置，当用户设置了其他配置时，此处无效，需要进一步完善
MDEDITOR_CONFIGS = MDConfig('default')

class admin_upload(UploadView):
    """ upload image file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(admin_upload, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT
        # image none check
        if not upload_image:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            }))

        # image format check
        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        # 替换上传图片名中非数字和字母的字符为'_'字符
        file_name_list = ["".join(filter(str.isalnum, _))
                          for _ in file_name_list]
        file_name = '.'.join(file_name_list)

        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    MDEDITOR_CONFIGS['upload_image_formats']),
                'url': ""
            }))

        # image floder check
        file_path = os.path.join(media_root, MDEDITOR_CONFIGS['image_floder'], '{0:%Y%m%d}'.format(
            datetime.datetime.now()))
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return HttpResponse(json.dumps({
                    'success': 0,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                }))

        # save image
        file_full_name = '%s_%s.%s' % (file_name,
                                       '{0:%Y%m%d%H%M}'.format(
                                           datetime.datetime.now()),
                                       file_extension)
        if not os.path.exists(os.path.join(file_path, file_full_name)):
            with open(os.path.join(file_path, file_full_name), 'wb+') as file:
                for chunk in upload_image.chunks():
                    file.write(chunk)
        res = HttpResponse(json.dumps({'success': 1,
                                       'message': "上传成功！",
                                       'url': '{0}{1}{2}/{3}/{4}'.format(settings.DOMAIN_NAME, settings.MEDIA_URL,
                                                                         MDEDITOR_CONFIGS['image_floder'], '{0:%Y%m%d}'.format(
                                           datetime.datetime.now()),
                                           file_full_name)}))
        return res



class default_upload(UploadView):
    """ upload image file """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(default_upload, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT
        # image none check
        if not upload_image:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            }))

        # image format check
        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        # 替换上传图片名中非数字和字母的字符为'_'字符
        file_name_list = ["".join(filter(str.isalnum, _))
                          for _ in file_name_list]
        file_name = '.'.join(file_name_list)

        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    MDEDITOR_CONFIGS['upload_image_formats']),
                'url': ""
            }))

        # image floder check
        file_path = os.path.join(media_root, 'mdeditor/uploads', '{0:%Y%m%d}'.format(
            datetime.datetime.now()))
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return HttpResponse(json.dumps({
                    'success': 0,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                }))

        # save image
        file_full_name = '%s_%s.%s' % (file_name,
                                       '{0:%Y%m%d%H%M}'.format(
                                           datetime.datetime.now()),
                                       file_extension)
        if not os.path.exists(os.path.join(file_path, file_full_name)):
            with open(os.path.join(file_path, file_full_name), 'wb+') as file:
                for chunk in upload_image.chunks():
                    file.write(chunk)
        res = HttpResponse(json.dumps({'success': 1,
                                       'message': "上传成功！",
                                       'url': '{0}{1}{2}/{3}/{4}'.format('http://'+request.get_host(), settings.MEDIA_URL,
                                                                         'mdeditor/uploads', '{0:%Y%m%d}'.format(
                                           datetime.datetime.now()),
                                           file_full_name)}))
        return res
