from django.db import models
from mdeditor.fields import MDTextField

import markdown
import emoji


class Comment(models.Model):
    # 评论者id
    author_id = models.IntegerField(verbose_name='评论者id')
    belong_article_id = models.IntegerField(verbose_name='所属文章id')
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    content = MDTextField('评论内容')
    parent_id = models.IntegerField(verbose_name='父级评论id')
    rep_to_id = models.IntegerField(verbose_name='回复评论id')
    is_deleted = models.BooleanField('是否已删除', default=False)
    class Meta:
        '''这是一个元类，用来继承的'''
        abstract = True

    def __str__(self):
        return self.content[:20]

    def content_to_markdown(self):
        # 先转换成emoji然后转换成markdown,'escape':所有原始HTML将被转义并包含在文档中
        to_emoji_content = emoji.emojize(self.content, use_aliases=True)
        to_md = markdown.markdown(to_emoji_content,
                                  safe_mode='escape',
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                  ])
        return to_md

# 留言板
class Message_Board(Comment):
    author_id = models.IntegerField(verbose_name='留言者id')
    message_parent_id = models.IntegerField(verbose_name='父级评论id')
    message_rep_id = models.IntegerField(verbose_name='回复评论id')
    is_deleted = models.BooleanField('是否已删除', default=False)
    
    class Meta:
        verbose_name = '网站留言'
        verbose_name_plural = verbose_name
        ordering = ['create_date']


class Comment_Notification(models.Model):
    create_user_id = models.IntegerField(verbose_name='所属评论id')
    recieve_user_id = models.IntegerField(verbose_name='所属评论id')
    comment_id = models.IntegerField(verbose_name='所属评论id')
    create_date = models.DateTimeField('提示时间', auto_now_add=True)
    is_read = models.BooleanField('是否已读', default=False)
    is_deleted = models.BooleanField('是否已删除', default=False)

    def mark_to_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

    class Meta:
        verbose_name = '提示信息'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return '{}@了{}'.format(self.create_p,self.get_p)