from django.shortcuts import render
from apps.blog.models import Article
from .models import ArticleComment, Notification, Message
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
user_model = settings.AUTH_USER_MODEL

#回复生成消息
def notify_handler(sender, instance, created, **kwargs):
    the_article = instance.belong
    create_p = instance.author
    # 判断是否是第一次生成评论，后续修改评论不会再次激活信号
    if created:
        if instance.rep_to:
            '''如果评论是一个回复评论，则同时通知给文章作者和回复的评论人，如果2者相等，则只通知一次'''
            if the_article.author == instance.rep_to.author:
                get_p = instance.rep_to.author
                if create_p != get_p:
                    new_notify = Notification(create_p=create_p, get_p=get_p, comment=instance)
                    new_notify.save()
            else:
                get_p1 = the_article.author
                if create_p != get_p1:
                    new1 = Notification(create_p=create_p, get_p=get_p1, comment=instance)
                    new1.save()
                get_p2 = instance.rep_to.author
                if create_p != get_p2:
                    new2 = Notification(create_p=create_p, get_p=get_p2, comment=instance)
                    new2.save()
        else:
            '''如果评论是一个一级评论而不是回复其他评论并且不是作者自评，则直接通知给文章作者'''
            get_p = the_article.author
            if create_p != get_p:
                new_notify = Notification(create_p=create_p, get_p=get_p, comment=instance)
                new_notify.save()

post_save.connect(notify_handler, sender=ArticleComment)


@login_required
@require_POST
def AddcommentView(request):
    if request.is_ajax():
        data = request.POST
        new_user = request.user
        new_content = data.get('content')
        rep_id = data.get('rep_id')
        try:
            # 如果能获得article_id，则添加文章评论
            article_id = data.get('article_id')
            the_article = Article.objects.get(id=article_id)
            if not rep_id:
                new_message = ArticleComment(author=new_user, content=new_content, belong=the_article, parent=None,
                                            rep_to=None)
            else:
                new_rep_to = ArticleComment.objects.get(id=rep_id)
                new_parent = new_rep_to.parent if new_rep_to.parent else new_rep_to
                new_message = ArticleComment(author=new_user, content=new_content, belong=the_article, parent=new_parent,
                                            rep_to=new_rep_to)
            new_message.save()
        except :
            # 如果不获得article_id，则添加留言板信息
            if not rep_id:
                new_message = Message(author=new_user, content=new_content, parent=None,
                                            rep_to=None)
            else:
                new_rep_to = Message.objects.get(id=rep_id)
                new_parent = new_rep_to.parent if new_rep_to.parent else new_rep_to
                new_message = Message(author=new_user, content=new_content, parent=new_parent, rep_to=new_rep_to)
            new_message.save()
            print(11111)
        
        new_point = '#mes-' + str(new_message.id)
        return JsonResponse({'msg': '评论提交成功！', 'new_point': new_point})
    return JsonResponse({'msg': '评论失败！'})

@login_required
def NotificationView(request, is_read=None):
    '''展示提示消息列表'''
    now_date = datetime.now()
    return render(request, 'comment/notification.html', context={'is_read': is_read, 'now_date': now_date})

@login_required
@require_POST
def mark_to_read(request):
    '''将一个消息标记为已读'''
    if request.is_ajax():
        data = request.POST
        user = request.user
        id = data.get('id')
        info = get_object_or_404(Notification, get_p=user, id=id)
        info.mark_to_read()
        return JsonResponse({'msg': 'mark success'})
    return JsonResponse({'msg': 'miss'})


@require_POST
def mark_to_delete(request):
    '''将一个成员删除'''
    if request.is_ajax():
        data = request.POST
        contacts = request.user
        member = data.get('id')
        info = get_object_or_404(Notification, contacts_p=contacts, member_p=member)
        info.delete()
        return JsonResponse({'msg': 'delete success'})
    return JsonResponse({'msg': 'miss'})

from django.views import generic

class MessageView(generic.ListView):
    model = Message
    template_name = 'comment/messages_board.html'
    context_object_name = 'leaved_messages'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(MessageView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-update_date', '-id')
        return ordering
