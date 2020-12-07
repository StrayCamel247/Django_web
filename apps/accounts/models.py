from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.models import TokenUser
from apps.api_exception import InvalidJwtToken, InvalidUser
from rest_framework_simplejwt.tokens import SlidingToken
from django.db import models
from django.contrib.auth.models import AbstractUser, User, AnonymousUser
from django.db.models.fields import IntegerField
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework import serializers
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from six import integer_types
from uuslug import slugify
from datetime import datetime
import random
from wsme import Unset
from apps.role.models import Role,RolePagePermission
from django.contrib.auth.hashers import check_password, make_password
from apps import system_name

from apps.utils.django_db import DBUtil
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
    系统用户基类，继承django抽象用户基类进行重构

    采用如下方法进行调用：
    >>> from django.contrib.auth import get_user_model
    >>> User = get_user_model()

    @staticmethod方法可以通过类直接调用
    >>> from django.contrib.auth import get_user_model
    >>> User = get_user_model()
    >>> User.xx_some_static_method_xx()
    """
    class Meta:
        verbose_name = """用户"""
        verbose_name_plural = verbose_name
        ordering = ['id']
        db_table = "{}_user".format(system_name)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    password = models.CharField(_('password'), max_length=128, null=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    link = models.URLField(
        '个人网址', blank=True, help_text='提示：网址必须填写以http开头的完整形式')
    contact = models.ManyToManyField(Contacts, verbose_name='通讯录', default='1')
    is_admin = models.BooleanField(verbose_name='管理员', default=False)
    is_deleted = models.BooleanField(verbose_name='已删除', default=False, null=True)
    introduction = models.TextField('个人简介', max_length=240, default='沉默是金😂')
    phone = models.TextField('电话号码', max_length=64, default='')
    # 扩展用户头像字段
    avatar = ProcessedImageField(
        upload_to='avatar/%Y%m%d',
        default='avatar/default/default ({}).jpg'.format(
            random.randint(0, 134)),
        verbose_name='头像',
        processors=[ResizeToFill(80, 80)],
        blank=True
    )

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

    def set_password(self, raw_password):
        """
        修改用户密码
        >>> python manage.py shell
        >>> from apps.accounts.models import Ouser
        >>> user=Ouser.objects.get(username='username')
        >>> user.set_password('new_password')
        """
        self.password = make_password(raw_password)
        self._password = raw_password
        self.save()

    @property
    def is_admin(self):
        """
        判断用户是否是管理员
        """
        return True if self.user_id == 1 else False

    def checkpassword(self, value: '待验证的密码'):
        """
        密码校验
        """
        if not self.password:
            return False
        return check_password(self.password, value)

    @property
    def is_authenticated(self):
        """
        验证用户是否登录
        """
        if isinstance(self, AnonymousUser):
            return False
        else:
            return True

    def is_del(self):
        """
        用户软删除机制
        判断用户是否删除
        """
        return self.is_delete

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUser):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def query_user_from_token(token: '用户动态jwt-token'):
        """
        将序列化的内容解码
        """
        User = get_user_model()
        _id = _token_get_user_id(token)
        _user = User.objects.get(id=_id)
        return _user

    @staticmethod
    def add_user(form):
        """
        增加用户,为用户新增角色
        """
        user_info = dict(username=form.username,
                         name=form.name,
                         password=form.password,
                         email=form.email,
                         phone=form.phone)
        roles = form.roles
        user = User(**user_info)
        user.save()

        # 赋予用户角色
        if len(roles) > 0:
            user_role_infos = [dict(
                user_id=user.get_id(),
                role_id=_
            ) for _ in roles]
            User_role.objects.bulk_create(user_role_infos)
        return user

    @staticmethod
    def update_user(form):
        """
        更新用户
        :param form:前端传入参数
        :return:
        """
        user_id = form.user_id
        username = form.username
        name = form.name
        email = form.email
        phone = form.phone
        remark = form.remark
        is_active = form.is_active
        roles = form.roles
        user = User.objects.get(user_id=user_id)

        user.username = username
        if email != Unset:
            user.email = email
        if phone != Unset:
            user.phone = phone
        if remark != Unset:
            user.remark = remark
        if is_active != Unset:
            user.is_active = is_active
        user.update_time = datetime.now()
        user.save()
        # 更新用户角色
        if roles != Unset:
            # 删除原先的用户角色
            User_role.objects.filter(user_id=user.id).delete()
            user_role_infos = [dict(
                user_id=user.get_id(),
                role_id=_
            ) for _ in roles]
            User_role.objects.bulk_create(user_role_infos)


class User_role(models.Model):
    class Meta:
        verbose_name = """用户角色关系表"""
        verbose_name_plural = verbose_name
        db_table = "{}_user_role".format(system_name)

    def __str__(self):
        return self.name
    # 角色id
    role_id = models.IntegerField(
        verbose_name=u"角色id")
    # 用户id
    user_id = models.IntegerField(
        verbose_name=u"角色id")
    
    is_deleted = models.BooleanField(verbose_name='已删除', default=False, null=True)

class UserInfoSerializer(HyperlinkedModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Ouser
        fields = ['username', 'introduction', 'avatar']

    def get_avatar(self, obj):
        # 拼接媒体url访问用户头像
        avatar_url = settings.HOST_MEDIA+obj.avatar.name
        return avatar_url


def _token_get_user_id(token):
    """
    The TokenUser class assumes tokens will have a recognizable user
    identifier claim.
    """
    try:
        Token = SlidingToken(token)
        assert api_settings.USER_ID_CLAIM in Token
        return TokenUser(Token).id
    except:
        raise InvalidJwtToken(
            detail='Token 失效')


def get_page_via_user(**params):
    """根据用户获取路由"""
    from ele_admin.base.models import PagePermission
    params = dict({
        'user_role_tablename': User_role._meta.db_table,
        'role_tablename': Role._meta.db_table,
        'role_page_permisson_talbename':RolePagePermission._meta.db_table,
        'ele_page_permisson':PagePermission._meta.db_table
    }, **params)
    sql = """
        with user_roles as(
            select u_r.role_id, u_r.user_id
            from public.{role_tablename} r
            left join public.{user_role_tablename} u_r on r.role_id = u_r.role_id
            where u_r.user_id = :user_id
        and r.is_active = true
        )
        , user_page_perm as
        (
            select 
                p_p.page_id, 
                p_p.page_name, 
                p_p.page_route, 
                p_p.page_path, 
                p_p.weight, 
                p_p.parent_id, 
                r_p.operation_type, 
                p_p.icon, 
                p_p.is_hidden
            from user_roles u_r
            left join public.{role_page_permisson_talbename} r_p 
                on u_r.role_id = r_p.role_id
                and r_p.is_deleted = false
            left join public.{ele_page_permisson} p_p 
                on p_p.is_deleted = false
                and p_p.basic = false 
                and r_p.page_id = p_p.page_id
            where r_p.operation_type = 1
            union all
            select 
                p_p.page_id, 
                p_p.page_name, 
                p_p.page_route, 
                p_p.page_path, 
                p_p.weight, 
                p_p.parent_id, 
                1 operation_type, 
                p_p.icon, 
                p_p.is_hidden
            from public.{ele_page_permisson} p_p 
            where p_p.basic = true
        )
        select 
            page_id, 
            page_name as title, 
            page_route as route, 
            page_path as path,
            weight, 
            parent_id
        from user_page_perm 
        group by page_id, page_name, page_route, page_path, weight, parent_id
        order by page_id, weight 
    """.format(**params)
    result = DBUtil.fetch_data_dict_sql(sql, params=params)
    return result

