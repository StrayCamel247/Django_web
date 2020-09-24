📚 Django 可视化项目

🐒 coders：[🐫Stray_camel](https://github.com/Freen247)

**☎ 联系方式**：
- prefer：[github/issue](https://github.com/Freen247/django_blog/issues)
- email：aboyinsky@outlook.com/wechat：1351975058

## ✨网站/规划功能/计划（Features/future）-持续更新...
- [x] index: 网站主要系统
    - [x] 规范的 Sitemap 网站地图、友情链接
    - [x] 强大的全文搜索功能，只需要输入关键词就能展现全站与之关联的文章
    - [x] 缓存系统、cdn加速、django（cache）缓存html界面、django-compress 压缩文件
    - [x] 支持RSS订阅`/api/rss/`

- [x] utils: 网站系统功能
    - [x] [创建网站数据类型，用于数据校验](django_server\apps\types.py)
    - [x] [自定义signature装饰器，应用于view模板，校验接口传参](django_server\apps\utils\wsme\signature.py)
    - [x] [自定义彩色日志系统，构建方法打印日志装饰器](django_server\apps\utils\log\handler.py)
    - [x] [重构django http请求方式校验](django_server\apps\utils\decorators\http.py)

- [x] data_analysis: 使用简单的numpy，pandas复现算法或者模型，并通过接口返回演示
    - `/data_analysis/compute_apriori/`:[Apriori算法实现](/django_server/apps/data_analysis/models/apriori.py)

- [x] models_sklearn_spark: 机器学习和各种模型算法小demo复现，并通过接口返回演示
    > 开发中...

- [x] models_tensorflow2: 使用tensorflow2复现论文，比赛等，并通过接口返回演示
    > 开发中...

- [x] api: 使用restful framework集成本网站的接口，对外开放，使用RESTful API框架，api主界面在`/api/v1/`
    - [x] 集合用户、博客、工具信息的api。

- [x] blog: 网站博客系统，basic 功能和界面展示、博客系统的文章分类（categories）、关键词（keywords）、浏览量统计以及规范的 SEO 设置。
    - [x] 文章的curd，展示文章、评论。

- [x] user: 用户认证系统，在 Django 自带的用户系统的基础上扩展 Oauth 认证，支持微博、Github 等第三方认证
    - [x] 邮箱注册登陆。
    - [x] 支持GitHub登陆，但还无法获取github用户头像。

- [x] comment: 评论系统，炫酷的输入框特效，支持 markdown 语法，二级评论结构和回复功能
    - [x] 网站评论功能，评论信息增删改查
    - [x] 支持表情包功能，已经增加特效
    - [x] 信息提醒功能，登录和退出提醒，收到评论和回复提醒，信息管理
    - [x] 网站留言板、聊天室功能, 对超过一天的留言或者评论信息可以进行撤回。

- [x] tool: 工具合集，扩展网站子工具，比如站内百度推送，爬虫，代码转化等
    >开发中...
    - [x] 百度sitemap/单链接站长推送工具
    - [x] User-Agent生成器, html特殊字符对照表, markdown在线编辑器, 友链测试工具
    - [x] 编辑文章可以粘贴图片上传, admin链接后台编辑和前端编辑界面上传路由不一样，具体文件在`tool/views.py`

 
## 🐾网站

- 项目运行（basic）
    > 大家有问题可以在[github issue](https://github.com/StrayCamel247/Django_React/issues/)戳我!
	
    - 让项目在服务器运行，参考文章：[Nginx + Gunicorn 服务器配置 Django](https://leetcode-cn.com/circle/article/6DA7GA/)
    - 服务器可使用`nohup bash gunicorn_start.sh`挂在后台运行。
    - 一键清除正在后台运行的django_blog项目，使用命令`bash kill_pid.sh`

    - 本地环境运行项目：
        - 安装pip需求包`pip install -r requirements.txt`
        -  更改`settings.py`文件中的数据库配置信息，使用本地`db.sqlite3`文件作数据库。
        - 构建项目所需要的数据库，连接信息更改请在`django_blog/settings.py`文件中进行更改
        - 链接新的数据库或者更换数据库需要运行`python manage.py makemigrations & python manage.py migrate`
        - 集合项目依赖包中的静态文件：`python manage.py collectstatic`
        - 压缩文件:`python manage.py compress`
        - 有问题欢迎到我网站留言和提issue

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


