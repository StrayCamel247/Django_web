from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.shortcuts import reverse
from uuslug import slugify
# 通讯录   category/contacts
class Contacts(models.Model):
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




# 继承 AbstractUser ，django 自带用户类，扩展用户个人网站字段，用户头像字段  article/members
# manytomany
# CASCADE   级联删除，此类选项模仿SQL语句ON DELETE CASCADE，再删除此字段信息的时候同时删除包含ForeignKey字段的目标（object）
# PROTECT 通过django.db.IntegrityError中的ProtectedError来保护此字段不被删除，若进行删除操作则抛出错误
# SET_NULL    将ForeignKey置为空，这只在null选项为True的时候产生作用
# SET_DEFAULT 设为默认值（default value），此默认值已预先对ForeignKey设置
# SET()   对ForeignKey设置对SET()函数传递的数值
# DO_NOTHING  不进行任何操作。若数据库提高了引用完整性，则此种设置会抛出一个IntegrityError，除非对这一数据字段手动添加了SQL语句中的ON DELETE字段

class Ouser(AbstractUser):
    # 扩展用户个人网站字段
    link = models.URLField('个人网址', blank=True, help_text='提示：网址必须填写以http开头的完整形式')
    contact = models.ManyToManyField(Contacts, verbose_name='通讯录',default='1')
    # 扩展用户头像字段
    avatar = ProcessedImageField(
        upload_to='avatar/%Y%m%d',
        default='avatar/default.png',
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
