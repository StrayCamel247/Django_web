"""
Django settings for django_blog project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1ek)3z+-*)(&1c&3fv=2*=lr_cyst85w&a4y#5!2m*ik@=&!p0'

# SECURITY WARNING: don't run with debug turned on in production!

# 自由选择需要开启的功能
# 是否开始[在线工具]应用
TOOL_FLAG = True
# 是否开启[API]应用
API_FLAG = False
# DEBUG模式是否开始的选择
# 值为0：所有平台关闭DEBUG,值为1:所有平台开启DEBUG,值为其他：根据平台类型判断开启（默认设置的Windows下才开启）
DEBUG = False
# 默认状态 COMPRESS_ENABLED=False，因为生产环境 DEBUG=False
# 只有在生产环境才有压缩静态资源的需求
# 如果是开发环境就主动开启压缩功能、开启手动压缩功能
if DEBUG:
    COMPRESS_ENABLED = True # 开启压缩功能
    COMPRESS_OFFLINE = True # 开启手动压缩
else:
    DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['boywithacoin.cn', '127.0.0.1','www.boywithacoin.cn']

SYSTEM_HOST = '127.0.0.1'
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'crispy_forms',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #apps
    'apps.blog',
    'apps.user',
    'apps.comment',
    'apps.tool',
    #lib
    'imagekit',  # 注册 imagekit处理压缩图片
    'mdeditor',#django mdeditor富文本编辑器
    'django.contrib.sitemaps',#网站地图
    'uuslug',#将中文转化成拼音 slug 的插件
    'markdown',#python自带的md翻译工具
    # allauth需要注册的应用    
    'django.contrib.auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
     # github 登陆 
    'allauth.socialaccount.providers.github',
    # 搜索
    'haystack',
    # 压缩
    'compressor',
    # rest框架
    # 'rest_framework',
]
# 如果需要在本地压缩，需要在settings.py中添加 COMPRESS_OFFLINE=True才能执行下边命令手动压缩
COMPRESS_OFFLINE=True
#mdeditor
MDEDITOR_CONFIGS = {
    'default':{
        'width': '90% ',  # Custom edit box width
        'heigth': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime"
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar 
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_floder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'syncScrolling': 'single',
        'sequence': True,  # Whether to open the sequence diagram function
    }
    
}
#搜索配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 选择语言解析器为自己更换的结巴分词
        'ENGINE': 'apps.blog.whoosh_cn_backend.WhooshEngine',
        # 保存索引文件的地址，选择主目录下，这个会自动生成
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
#指定什么时候更新索引，这里定义为每当有文章更新时就更新索引。由于博客文章更新不会太频繁，因此实时更新没有问题。
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# redis缓存配置
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# 登陆成功后的回调路由
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
AUTHENTICATION_BACKENDS = (
    # auth 身份验证 与 allauth 无关
    'django.contrib.auth.backends.ModelBackend',
    # allauth 身份验证 
    'allauth.account.auth_backends.AuthenticationBackend',
)


# 网站信息设置 用于SEO
SITE_DESCRIPTION = "Stray_Camel的个人技术博客，django_blog，django2.0+python3技术搭建。"
SITE_KEYWORDS = "Stray_Camel,django2.0博客，人工智能,网络,IT,技术,博客,Python"

AUTHOR_NAME = "Stray_Camel"
AUTHOR_DESC = 'early to bed, early to rise.'
AUTHOR_EMAIL = 'aboyinsky@outlook.com'
AUTHOR_TITLE = 'rookie'

# Email setting
# SMTP服务器，我使用的是sendclound的服务
# 是否使用了SSL 或者TLS
#EMAIL_USE_SSL = True
#EMAIL_USE_TLS = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.outlook.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aboyinsky@outlook.com'
EMAIL_HOST_PASSWORD = '1026shenyang'
DEFAULT_FROM_EMAIL = 'aboyinsky@outlook.com'


# 这里是随便写的一个 也可以是 /accounts/logout/ 测试比较随便
LOGIN_REDIRECT_URL = '/'
# 要求用户注册时必须填写email
ACCOUNT_EMAIL_REQUIRED = True
# 注册中邮件验证方法:“强制（mandatory）”,“可选（optional）【默认】”或“否（none）”之一。
# 开启邮箱验证的话，如果邮箱配置不可用会报错，所以默认关闭，根据需要自行开启
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# 作用于第三方账号的注册
# SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional' | 'mandatory' | 'none'
# 邮件发送后的冷却时间(以秒为单位)
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 10
# # 邮箱确认邮件的截止日期(天数)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

# # 指定要使用的登录方法(用户名、电子邮件地址或两者之一)"username" | "email" | "username_email"
ACCOUNT_AUTHENTICATION_METHOD="username_email"
# # 登录尝试失败的次数
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT(=5)
# # 从上次失败的登录尝试，用户被禁止尝试登录的持续时间
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT(=300)
# # 更改为True，用户一旦确认他们的电子邮件地址，就会自动登录
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# # 更改或设置密码后是否自动退出
# ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE(=False)
# 更改为True，用户将在重置密码后自动登录
ROOT_URLCONF = 'blog.urls'

AUTH_USER_MODEL = 'user.Ouser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
db_table = 'user'
ROOT_URLCONF = 'django_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #全局变量
                'apps.blog.views.global_setting',
                # allauth 需要 django 提供这个处理器
                'django.template.context_processors.request',
            ],
        },
    },
]
# 位于django.contrib.sites的site。
# SITE_ID指定与特定配置文件相关联的site对象之数据库的ID。
# 当出现"SocialApp matching query does not exist"，这种报错的时候就需要更换这个ID
SITE_ID = 1
WSGI_APPLICATION = 'django_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dbblog',
#         'USER': 'root',
#         'PASSWORD': '1026shenyang',
#         'HOST': 'LOCALHOST',
#         'PORT': '3306'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 有改动

TIME_ZONE = 'Asia/Shanghai'  # 有改动

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',)
# 静态文件收集
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),
    # 'static/',
    #debug模式服务器解决后端admin界面css样式缺失
    # '/home/django_blog/env/lib/python3.6/site-packages/django/contrib/admin/static'
]
#媒体文件
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')



# 统一分页设置
#指定如何对搜索结果分页，这里设置为每 10 项结果为一页。
BASE_PAGE_BY = 7
BASE_ORPHANS = 4

