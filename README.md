📚 Django 开发的个人网站

🐒 coders：[🐫Stray_camel](https://github.com/Freen247)。

**☎ 商业合作/联系方式**：
- [prefer：github/issue](https://github.com/Freen247/django_blog/issues)
- email：aboyinsky@outlook.com/wechat：1351975058

## ✨网站/规划功能/计划（Features/future）-持续更新...
> 使用 Django 自带的后台管理系统，方便对于文章、用户及其他动态内容的管理

- [x] App（index）：网站主要系统，basic 功能和界面展示、博客系统的文章分类（categories）、关键词（keywords）、浏览量统计以及规范的 SEO 设置。
    - [x] 规范的 Sitemap 网站地图、友情链接
    - [x] 强大的全文搜索功能，只需要输入关键词就能展现全站与之关联的文章
    - [x] 缓存系统、cdn加速、django（cache）缓存html界面、django-compress 压缩文件
    - [x] 支持RSS订阅

- [x] App（api）：集成本网站的接口，对外开放，使用RESTful API框架，api主界面在`/api/v1/`
    - [x] 集合所有用户信息的api。
    - [x] 集合所有博客信息的api。
    - [x] 集合所有工具信息的api。

- [x] App（blog）：网站博客系统，basic 功能和界面展示、博客系统的文章分类（categories）、关键词（keywords）、浏览量统计以及规范的 SEO 设置。
    - [x] 文章的curd，展示和评论集合功能，作为网站的展示首页

- [x] App（user）用户认证系统，在 Django 自带的用户系统i的基础上扩展 Oauth 认证，支持微博、Github 等第三方认证
    - [ ] 扩展个人中心界面，设置二级权限，让认证的人能够发送留言。-开发中..
    - [ ] 支持订阅其他网站的文章信息，统一使用restful api风格。-开发中..

- [x] App（comment）评论系统，炫酷的输入框特效，支持 markdown 语法，二级评论结构和回复功能
    - [x] 支持表情包功能，已经增加特效
    - [x] 信息提醒功能，登录和退出提醒，收到评论和回复提醒，信息管理

- [x] App（tool）工具合集，扩展网站子工具，比如站内百度推送，爬虫，代码转化等
    - [x] 百度sitemap/单链接站长推送工具
    - [x] markdown在线编辑器
    - [x] User-Agent生成器
    - [x] html特殊字符对照表
    - [x] 友链测试工具
    - [ ] 豆瓣电影爬虫工具-开发中..
    - [ ] 添加图床服务器、编辑文章可以粘贴图片上传等-开发中..

- [ ] App（ml_rec）上线网站推荐系统demo
    - [ ] 开发中...
 
## 🐾网站开发日志（How to contribute this webproject？）
> 欢迎大家一起和我contribute，扩展更多的功能。

1. 使用 markdown 语言来编写文章（basic）
    - [markdown基本语法](https://boywithacoin.cn/article/markdownji-ben-yu-fa/)
2. 克隆 clone 项目后让项目在服务器运行（basic）
    > 大家有问题可以在[网站评论](https://boywithacoin.cn/)或者[github issue](https://github.com/Freen247/django_blog/issues)戳我!
	
    - [Nginx + Gunicorn 服务器配置 Django](https://boywithacoin.cn/article/nginx-gunicorn-fu-wu-qi-pei-zhi-django/)

3. 利用django开发网站日志
    >类似于开发手册/教程，希望可以一起来contribute，支持更多的功能或框架！
    - [网站开发日志/教程](https://boywithacoin.cn/timeline)
    
4. 依赖包
    - model_requirements.txt为本地跑模型需要使用的依赖包
    - requirements.txt为项目运行的依赖包

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
![Python](https://boywithacoin.cn/static/media/editor/TIM%E5%9B%BE%E7%89%872020010122455_20200101225818752500.png)

