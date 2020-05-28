from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import time

# Create your models here.

class ToolCategory(models.Model):
    name = models.CharField('网站分类名称', max_length=20)
    order_num = models.IntegerField('序号', default=99, help_text='序号可以用来调整顺序，越小越靠前')

    class Meta:
        verbose_name = '工具分类'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name
#自定义自动修改上传的图片的图片名，并修改图片形式为png


class ImageStorage(FileSystemStorage):

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        #初始化
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        #重新文件上传
        import hashlib
        #获取文件后缀
        ext = '.bmp'
        #文件目录
        d = os.path.dirname(name)
        #定义文件夹名称
        fn = hashlib.md5(time.strftime(
            '%Y-%m-%d-%H-%M-%S').encode('utf-8')).hexdigest()
        name = os.path.join(d, fn+ext)

        #调用父类方法
        return super(ImageStorage, self)._save(name, content)
class ToolLink(models.Model):
    name = models.CharField('网站名称', max_length=20)
    description = models.CharField('网站描述', max_length=100)
    link = models.URLField('网站链接')
    order_num = models.IntegerField('序号', default=99, help_text='序号可以用来调整顺序，越小越靠前')
    category = models.ForeignKey(ToolCategory,on_delete=models.CASCADE, verbose_name='网站分类',blank=True,null=True)
    img = models.ImageField(upload_to='media/tool', blank=True, null=True,
                            default="/static/images/summary.jpg", storage=ImageStorage())
    class Meta:
        verbose_name = '工具'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name


