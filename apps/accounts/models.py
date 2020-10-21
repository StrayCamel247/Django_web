from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import IntegerField
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from six import integer_types
from uuslug import slugify
from datetime import datetime
import random

# 用户注册
def user_register(request):
    '''
    用户注册视图函数
    :param request:
    :return:
    '''
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
def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.1117.link的注册确认邮件'

    text_content = '''欢迎注册www.1117.link，这里是大鱼的论坛站点，专注于Python和Django技术的分享！\
                        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                        <p>感谢注册<a href="http://{}/user/confirm/?code={}" target=blank>www.1117.link</a>，\
                        这里是大鱼的博客和教程站点，专注于Python和Django技术的分享！</p>
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1:80', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")

    msg.send()

class Contacts(models.Model):
    """通讯录   category/contacts"""
    name = models.CharField('通讯录', max_length=20)
    description = models.TextField('描述', max_length=240, default="通讯录",
                                   help_text='用来作为SEO中description,长度参考SEO标准')
    slug = models.SlugField(unique=False)

    class Meta:
        verbose_name = '通讯录'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user:contacts', kwargs={'slug': self.slug})

    def get_members_list(self):
        return Ouser.objects.filter(contacts=self)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Contacts, self).save(*args, **kwargs)


class Ouser(AbstractUser):
    """
    AbstractUser ，django 自带用户类，扩展用户个人网站字段，用户头像字段  article/members
    manytomany
    CASCADE   级联删除，此类选项模仿SQL语句ON DELETE CASCADE，再删除此字段信息的时候同时删除包含ForeignKey字段的目标（object）
    PROTECT 通过django.db.IntegrityError中的ProtectedError来保护此字段不被删除，若进行删除操作则抛出错误
    SET_NULL    将ForeignKey置为空，这只在null选项为True的时候产生作用
    SET_DEFAULT 设为默认值（default value），此默认值已预先对ForeignKey设置
    SET()   对ForeignKey设置对SET()函数传递的数值
    DO_NOTHING  不进行任何操作。若数据库提高了引用完整性，则此种设置会抛出一个IntegrityError，除非对这一数据字段手动添加了SQL语句中的ON DELETE字段
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True, unique=True)
    link = models.URLField(
        '个人网址', blank=True, help_text='提示：网址必须填写以http开头的完整形式')
    contact = models.ManyToManyField(Contacts, verbose_name='通讯录', default='1')
    introduction = models.TextField('个人简介', max_length=240, default='沉默是金😂')
    # 扩展用户头像字段
    avatar = ProcessedImageField(
        upload_to='avatar/%Y%m%d',
        default='avatar/default/default ({}).jpg'.format(
            random.randint(0, 134)),
        verbose_name='头像',
        processors=[ResizeToFill(80, 80)],
        blank=True
    )

    class Meta:
        verbose_name = '用户'  # 定义网站管理后台表名
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        x = Contacts(name=self.username)
        if (Contacts.objects.filter(name=self.username)):
            # self.contact.set(Contacts.objects.filter(name=self.username))
            pass
        else:
            x.save()
        super(Ouser, self).save(*args, **kwargs)

    def db_delete_user(self):
        deleteResult = Ouser.objects.filter(username=self.username).delete()
        if deleteResult:
            return 1

    def test(self):
        return 222


class User_role(models.Model):
    class Meta:
        verbose_name = """用户角色关系表"""
        verbose_name_plural = verbose_name
        db_table = "user_role"

    def __str__(self):
        return self.name
    # 角色id
    role_id = models.IntegerField(
        verbose_name=u"角色id")
    # 用户id
    user_id = models.IntegerField(
        verbose_name=u"角色id")

class UserInfoSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Ouser
        fields = ['id', 'username', 'introduction','avatar']