from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import jwt
from apps.utils.core.http import require_http_methods
from apps.utils.wsme.signature import signature
from .types import AccountsResult, AccountLoginBody, AccountTokenBody, AccountRefreshBody
from .forms import ProfileForm
from .models import Contacts, Ouser
from .handler import token_refresh_sliding_handler, token_obtain_sliding_handler, token_refresh_handler, token_obtain_pair_handler, token_verify_handler,token_user_info_handler,token_user_password_change_handler,AccountPasswordChangeBody
# Create your views here.
urlpatterns = []

@require_http_methods('account/access-login', methods=['POST'])
@signature(AccountsResult, body=AccountLoginBody)
def token_obtain_pair(body):
    params = {
        'username': body.username,
        'password': body.password
    }
    content = token_obtain_pair_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/access-refresh', methods=['POST'])
@signature(AccountsResult, body=AccountRefreshBody)
def token_access_refresh(body):
    params = {
        'refresh': body.refresh
    }
    content = token_refresh_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token-login', methods=['POST'])
@signature(AccountsResult, body=AccountLoginBody)
def token_obtain_sliding(body):
    params = {
        'username': body.username,
        'password': body.password
    }
    content = token_obtain_sliding_handler(**params)
    return AccountsResult(content=content)


@require_http_methods('account/token-refresh', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_refresh(body):
    params = {
        'token': body.token
    }
    content = token_refresh_sliding_handler(**params)
    return AccountsResult(content=content)

@require_http_methods('account/token-verify', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_verify(body):
    params = {
        'token': body.token
    }
    content = token_verify_handler(**params)
    return AccountsResult(content=content)

@require_http_methods('account/user_info', methods=['POST'])
@signature(AccountsResult, body=AccountTokenBody)
def token_user_info(body):
    params = {
        'token': body.token
    }
    content = token_user_info_handler(**params)
    return AccountsResult(content=content)

@require_http_methods('account/user_password_change', methods=['POST'], jwt_required=True)
@signature(AccountsResult, body=AccountPasswordChangeBody)
def token_user_password_change(body):
    params = {
        'id': body.id,
        'username': body.username,
    }
    content = token_user_password_change_handler(**params)
    return AccountsResult(content=content)

## v1.0
@login_required
def users_view(request):
    return render(request, 'user/users.html')


@login_required
def profile_view(request):
    return render(request, 'user/account/profile.html')


@login_required
def change_profile_view(request):
    if request.method == 'POST':
        # 上传文件需要使用request.FILES
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # 添加一条信息,表单验证成功就重定向到个人信息页面
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功！')
            return redirect('accounts:profile')
    else:
        # 不是POST请求就返回空表单
        form = ProfileForm(instance=request.user)
    return render(request, 'user/account/change_profile.html', context={'form': form})


@login_required
def AdminView(request):
    # if request.method == 'POST':
    #     # 上传文件需要使用request.FILES
    #     form = ProfileForm(request.POST,request.FILES,instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         # 添加一条信息,表单验证成功就重定向到个人信息页面
    #         messages.add_message(request,messages.SUCCESS,'个人信息更新成功！')
    #         return redirect('accounts:profile')
    # else:
    #     # 不是POST请求就返回空表单
    #     form = ProfileForm(instance=request.user)
    return render(request, 'user/account/admin.html')


# @csrf_exempt
@require_POST
def DelmemberView(request):
    '''将一个member删除'''
    if request.is_ajax():
        data = request.POST
        # if (data):
        #     JsonResponse({'msg': 'good'})
        member_id = data.get('member_id')
        contact_id = data.get('contact_id')
        # JsonResponse({'msg': 'good'})
        member = get_object_or_404(Ouser, id=member_id)
        cont = get_object_or_404(Contacts, id=contact_id)
        # 获取当前通讯录下所有的用户列表
        member.contact.remove(cont)
        # info.delete()
        # if (info):
        # return JsonResponse({'msg': })
        # else :
        #     return JsonResponse({'msg': 'delete success'})

    return JsonResponse({'msg': contact_id})


@require_POST
def AddmemberView(request):
    '''增加member'''
    if request.is_ajax():
        data = request.POST
        # if (data):
        #     JsonResponse({'msg': 'good'})
        member_id = data.get('member_id')
        contact_id = data.get('contact_id')
        # JsonResponse({'msg': 'good'})
        member = get_object_or_404(Ouser, id=member_id)
        cont = get_object_or_404(Contacts, id=contact_id)
        member.contact.add(cont)
        # info.delete()
        # if (info):
        #     return JsonResponse({'msg': })
        # else :
        #     return JsonResponse({'msg': 'delete success'})

    return JsonResponse({'msg': "good"})


@require_POST
def SearchmemberView(request):
    '''搜索member'''
    if request.is_ajax():
        data = request.POST
        member_id = data.get('member_id')
        member_name = data.get('member_name')

        if (get_object_or_404(Ouser, id=member_id).username == member_name):
            return JsonResponse({'msg': member_id})
        else:
            return JsonResponse({'msg': 'nobody'})


class ContactsView(generic.ListView):
    model = Ouser
    template_name = 'user/contacts.html'
    context_object_name = 'members'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_queryset(self, **kwargs):
        queryset = super(ContactsView, self).get_queryset()
        contacts = get_object_or_404(Contacts, slug=self.kwargs.get('slug'))
        return queryset.filter(contact=contacts)

    def get_context_data(self, **kwargs):
        context_data = super(ContactsView, self).get_context_data()
        contacts = get_object_or_404(Contacts, slug=self.kwargs.get('slug'))
        context_data['search_contacts'] = '通讯录'
        context_data['search_instance'] = contacts
        return context_data
