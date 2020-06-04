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
from django.views import generic

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
    if not request.is_ajax():return JsonResponse({'msg': '评论失败！'})
    data = request.POST
    user = request.user
    new_content = data.get('content', None)
    rep_id = data.get('rep_id', None)
    article_id = data.get('article_id', None)
    new_rep_to = (ArticleComment.objects.get(id=rep_id) if rep_id!='' else None) if article_id!='' else (Message.objects.get(id=rep_id) if rep_id!='' else None)
    # 评论/留言的层级
    try:
        new_parent = new_rep_to.parent if new_rep_to.parent else new_rep_to
    except AttributeError:
        new_parent = None
    # 文章评论或者为留言板留言
    new_message = (ArticleComment(author=user, content=new_content, belong=Article.objects.get(id=article_id), parent=new_parent, rep_to=new_rep_to)) if article_id!='' else (Message(author=user, content=new_content, parent=new_parent, rep_to=new_rep_to))
    new_message.save()
    
    new_point = '#mes-' + str(new_message.id)
    return JsonResponse({'msg': '评论提交成功！', 'new_point': new_point})
    
@login_required
@require_POST
def DelcommentView(request):
    if not request.is_ajax():return JsonResponse({'msg': '评论失败！'})
    data = request.POST
    user = request.user
    mes_id = data.get('mes_id', None)
    article_id = data.get('article_id', None)
    message = get_object_or_404(ArticleComment, author=user, belong=Article.objects.get(id=article_id), pk=mes_id) if article_id!=None else get_object_or_404(Message, author=user, pk=mes_id)
    message.delete()
    return JsonResponse({'msg': 'delete success'})

@login_required
def NotificationView(request, is_read=None):
    '''展示提示消息列表'''
    now_date = datetime.now()
    return render(request, 'comment/notification.html', context={'is_read': is_read, 'now_date': now_date})

@login_required
@require_POST
def mark_to_read(request):
    """编辑文章评论消息已读"""
    if not request.is_ajax():return JsonResponse({'msg': '标记失败！'})
    data = request.POST
    user = request.user
    notification_id = data.get('id')
    info = get_object_or_404(Notification, get_p=user, id=id)
    info.mark_to_read()
    return JsonResponse({'msg': 'mark success'})


@require_POST
def mark_to_delete(request):
    """删除文章评论消息通知"""
    if not request.is_ajax():return JsonResponse({'msg': '删除失败！'})
    data = request.POST
    user = request.user
    notification_id = data.get('id')
    info = get_object_or_404(Notification, get_p=user, id=notification_id)
    info.delete()
    return JsonResponse({'msg': 'delete success'})


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
        return ('-id',)
