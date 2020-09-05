📚 Django+bootstrap4开发的博客网站

**☎ 联系方式**：
- prefer：[github/issue](https://github.com/Freen247/django_blog/issues)
- email：aboyinsky@outlook.com/wechat：1351975058

## 🐾网站

- 项目运行（basic）
    > 大家有问题可以在[github issue](https://github.com/Freen247/django_blog/issues)戳我!
	- /amdin 超级管理用户为 admin, test123890
    - 让项目在服务器运行，参考文章：[Nginx + Gunicorn 服务器配置 Django]()
    - 服务器可使用`nohup bash gunicorn_start.sh`挂在后台运行。
    - 一键清除正在后台运行的django_blog项目，使用命令`bash kill_pid.sh`

    - 本地环境运行项目：
        - 配置了新命令`python .\manage.py clear_migrations`，可以清楚所有makemigrations文件
        - 安装pip需求包`pip install -r requirements.txt`
        - 更改`settings.py`文件中的数据库配置信息，使用本地`db.sqlite3`文件作数据库。
        - 构建项目所需要的数据库，连接信息更改请在`django_blog/settings.py`文件中进行更改
        - **链接新的数据库或者更换数据库需要运行：**`python manage.py makemigrations & python manage.py migrate`
        - **集合项目依赖包中的静态文件：**`python manage.py collectstatic`
        - **压缩文件:**`python manage.py compress`
        - **运行网站:**`python manage.py runserver`
        - 有问题欢迎到我网站留言和提issue

- 依赖包
    - requirements.txt为项目运行的依赖包

## ✨网站功能/计划
> 使用 Django 自带的后台管理系统，自定义开发接口和界面。

- [x] App（index）：网站主要系统，basic 功能和界面展示、博客系统的文章分类（categories）、关键词（keywords）、浏览量统计以及规范的 SEO 设置。
    - [x] 规范的 Sitemap 网站地图、友情链接
    - [x] 强大的全文搜索功能，只需要输入关键词就能展现全站与之关联的文章
    - [x] 缓存系统、cdn加速、django（cache）缓存html界面、django-compress 压缩文件
    - [x] 支持RSS订阅`/api/rss/`

- [x] App（api）：使用restful framework集成本网站的接口，对外开放，使用RESTful API框架，api主界面在`/api/v1/`
    - [x] 集合用户、博客、工具信息的api。

- [x] App（blog）：网站博客系统，basic 功能和界面展示、博客系统的文章分类（categories）、关键词（keywords）、浏览量统计以及规范的 SEO 设置。
    - [x] 文章的curd，展示文章、评论。

- [x] App（user）用户认证系统，在 Django 自带的用户系统的基础上扩展 Oauth 认证，支持微博、Github 等第三方认证
    - [x] 邮箱注册登陆。
    - [x] 支持GitHub登陆。

- [x] App（comment）评论系统，炫酷的输入框特效，支持 markdown 语法，二级评论结构和回复功能
    - [x] 网站评论功能，评论信息增删改查
    - [x] 支持表情包功能，已经增加特效
    - [x] 信息提醒功能，登录和退出提醒，收到评论和回复提醒，信息管理
    - [x] 网站留言板、聊天室功能, 对超过一天的留言或者评论信息可以进行撤回。

- [x] App（tool）工具合集，扩展网站子工具，比如站内百度推送，爬虫，代码转化等
    - [x] 百度sitemap/单链接站长推送工具
    - [x] markdown在线编辑器
    - [x] User-Agent生成器
    - [x] html特殊字符对照表
    - [x] 友链测试工具
    - [x] 编辑文章可以粘贴图片上传, admin链接后台编辑和前端编辑界面上传路由不一样，具体文件在`tool/views.py`

- [x] 此django一站式项目目前开发完毕，目前更新项目为前后端分离项目在[Django_React](https://github.com/StrayCamel247/Django_React)
    > 项目更加完整，接口化更加规范，项目集成可扩展app管理，目标在开发多个页面和多种功能。
    > 前端样式继承此套接口，将样式原封不动的迁移到react中


## 🌲源码分支管理：
- [webiste_files](https://github.com/Freen247/django_blog/tree/website_files)：当前目录为网站前端样式的初始化文件。利用框架有bootstrap，fontawsome。

## 🤹‍♀️FAQ
1. 为何不适用其他的 xadmin 等后台管理系统？
    - 🐫：因为自带的 admin 包已经完全满足了我的需求、而且我个人是准备来开发一个个人主页的（可以 curd 文章和其他信息之类的）
2. 博主的网站建设是完全自己写出来的吗？文章之类的也是完全自己想出来的吗？
    - 🐫：并不是！其实网上开发这种博客系统的东西有很多先例了，我也算是在这条线跟着别人学然后入门吧，只是以后想扩展更多的功能在上面。

## 🙃常见安装项目 bug
- `ImportError: PILKit was unable to import the Python Imaging Library. Please confirm it`s installe...`
    - 安装pillow库：`pip install pillow`

- `ModuleNotFoundError: No module named 'compressor'`
    - 原因是安装django_compressor时的依赖包rcssm出了问题，重新安装rcssm包
    - `pip install rcssmin --install-option="--without-c-extensions"`

- `ImportError: cannot import name 'connections' from 'haystack' `
    - 常见处理方法；写在自动安装的依赖包`pip uninstall haystack`，如果还不能解决，重新卸载并安装djang-haystack。

- `ImportError: cannot import name 'ChineseAnalyzer' from 'jieba.analyse' (F:\workspac' `
    - 安装依赖包`whoosh`，其实在requirement里面已经有了，但是估计时没安装成功吧。再安装一次就好了

- `ModuleNotFoundError: No module named 'user_agent'`
    - 这个包直接安装就好，` pip install user_agent`

- 数据库迁移/项目运行bug：`ValueError : unsupported pickle protocol: 5`
    - 这个bug根据pick协议，我们的查询功能whoosh功能时当我们访问这个页面，就将信息缓存下来，由于服务器py版本和win版本不一样可能会导致这个问题，解决方法就是删除项目中`django_blog\whoosh_index`文件夹中的所有文件。

## 🐒网站实际效果预览
![Python](./template.png)

