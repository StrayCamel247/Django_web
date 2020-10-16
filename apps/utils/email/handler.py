#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 邮箱发送脚本，用在用户注册、验证等功能
# __REFERENCES__ :
# __date__: 2020/10/16 17
import datetime
import pytz

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password, check_password


from django.conf import settings


def make_confirm_string(user):
    from uuid import uuid4
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = str(uuid4())
    models.ConfirmString.objects.create(code=code, user=user)
    return code

# 用户注册
def user_register(**kwargs):
    if request.session.get('is_login', None):
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'user/user_register.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        email = request.POST.get('email')
        try:
            user = models.User.objects.get(username=username)
            return render(request, 'user/user_register.html', {'error_code': -1, 'error_msg': '账号已经存在,换个账号试试吧!'})
        except:
            try:
                user = models.User.objects.get(email=email)
                return render(request, 'user/user_register.html',
                              {'error_code': -2, 'error_msg': '邮箱已经存在,换个昵称试试吧!'})
            except:
                if password != re_password:
                    return render(request, 'user/user_register.html',
                                  {'error_code': -3, 'error_msg': '两次密码输入不一致,请重新注册'})
                else:
                    password = make_password(password, None, 'pbkdf2_sha256')
                    user = models.User(username=username,
                                       password=password, email=email)
                    user.save()
                    code = make_confirm_string(user)
                    send_email(email, code)

                    message = '请前往注册邮箱，进行邮件确认！'
                    return render(request, 'user/confirm.html', locals())

# 邮箱发送
def send_email(**kwargs):
    """邮件发送"""
    from django.core.mail import EmailMultiAlternatives
    subject = '邮箱发送'
    text_content = '''如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''感谢注册'''
    to_email = kwargs.get('email')
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'user/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'user/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '恭喜您注册成功，赶快尝试登录吧！'
        return render(request, 'user/confirm.html', locals())
