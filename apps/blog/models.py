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
# Create your models here.
#自定义自动修改上传的图片的图片名，并修改图片形式为png






# 网站导航菜单栏分类表
# 文章分类
class Category(models.Model):
    name = models.CharField('文章分类', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)

# 文章关键词，用来作为 SEO 中 keywords
class Keyword(models.Model):
    name = models.CharField('文章关键词', max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

# 友情链接表
class FriendLink(models.Model):
    name = models.CharField('网站名称', max_length=50)
    description = models.CharField('网站描述', max_length=100, blank=True)
    link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址')
    logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否有效', default=True)
    is_show = models.BooleanField('是否首页展示', default=False)

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

# 时间线
class Timeline(models.Model):
    #选择在左边显示还是右边
    SIDE_CHOICE = (
        ('L', '左边'),
        ('R', '右边'),
    )
   
    side = models.CharField(
        '位置', max_length=1, choices=SIDE_CHOICE, default='L')
    icon = models.CharField('图标', max_length=50, default='fa fa-pencil')
    title = models.CharField('标题', max_length=100)
    update_date = models.DateTimeField('更新时间')
    content = models.TextField('主要内容')
    #唯一标识符
    slug = models.SlugField(editable=False,null=True, unique=True)
    class Meta:
        verbose_name = '博客升级时间线'
        verbose_name_plural = verbose_name
        ordering = ['-update_date']

    def __str__(self):
        return self.title[:20]

    def get_timeline_list(self):
        """返回所有文章列表"""
        return Timeline.objects.all()

    def title_to_emoji(self):
        return emoji.emojize(self.title, use_aliases=True)

    def content_to_markdown(self):
        # 先转换成emoji然后转换成markdown
        to_emoji_content = emoji.emojize(self.content, use_aliases=True)
        return markdown.markdown(to_emoji_content,
                                 extensions=['markdown.extensions.extra',
                                 'markdown.extensions.codehilite'
                                  ]
                                 )

    def save(self, *args, **kwargs):
            self.slug = slugify(self.title)
            super(Timeline, self).save(*args, **kwargs)

# 文章
class Article(models.Model):
    # 文章作者
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者', null=False, default='2')
    title = models.CharField(max_length=150, verbose_name='文章标题')
    summary = models.TextField(
        '文章摘要', max_length=230, default='文章摘要等同于网页description内容，请务必填写...')
    # 文章内容
    body = MDTextField(verbose_name='文章内容')
    create_date = models.DateTimeField(verbose_name='创建时间')
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('阅览量', default=0)

    img = models.ImageField(upload_to='article/%Y%m%d',
                            default='artile/default.png', storage=ImageStorage())
    # 文章唯一标识符
    slug = models.SlugField(editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='文章分类', null=False, default='2')
    keywords = models.ManyToManyField(Keyword, verbose_name='文章关键词',
                                      help_text='文章关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    #置顶
    is_top = models.BooleanField('是否首页展示', default=False)
    #是否更新timeline
    is_addtimeline = models.BooleanField('是否添加时间线', default=False)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-update_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'slug': self.slug})

    def summary_to_markdown(self):
        return markdown.markdown(self.summary, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_num(self):
        return Article.objects.filter(id__lt=self.id).count()

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()

    #添加到博客开发时间线
    def add_time(self):
        web_time = Timeline()
        web_time.title = self.title
        web_time.content = self.summary
        web_time.icon = self.img
        web_time.update_date = self.create_date
        web_time.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # 讲中文title变成拼音。
        #在添加文章时手动选择是否添加到开发日志
        if(self.is_addtimeline):
            try:
                #如何只是对文章进行修改，说明已经添加过
                if(Timeline.objects.get(slug=self.slug)):
                    #则只对日志中的内容和图片和时间进行修改。
                    old = Timeline.objects.get(slug=self.slug)
                    old.content = self.summary
                    old.icon = self.img
                    old.update_date = self.create_date
                    old.save(update_fields=['content', 'icon','update_date'])
                else:
                    #如果没有添加过则就直接创建日志再发布
                    self.add_time()
                    #objects.get可能的报错
            except Timeline.DoesNotExist:
                self.add_time()
            except Timeline.MultipleObjectsReturned:
                pass
        super(Article, self).save(*args, **kwargs)
