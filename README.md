📚 Django 开发的个人网站

🐒 coders：[🐫Stray_camel](https://github.com/Freen247)。

🐾 希望大家一起来contribute or fork👍！

**☎ contact me**：
- [prefer：github/issue](https://github.com/Freen247/django_blog/issues)
- email：aboyinsky@outlook.com/wechat：1351975058

## ✨网站功能/计划（Features/future）
> 网站是基于博客系统建立起来的，不仅仅局限于这个功能。在这个层面上会更加扩展地开发更多的功能。

- [x] 使用 Django 自带的后台管理系统，方便对于文章、用户及其他动态内容的管理
- [x] App（index）网站主要系统，basic 功能和界面展示
    - [x] 缓存系统、cdn加速、django（cache）缓存html界面、django-compress 压缩文件
    - [x] 规范的 Sitemap 网站地图、友情链接
    - [x] 常见的RESTful API 风格的 API 接口
- [x] App（blog）：博客系统的文章分类（categories）、关键词（keywords）、浏览量统计以及规范的 SEO 设置
    - [x] 强大的全文搜索功能，只需要输入关键词就能展现全站与之关联的文章
- [x] App（user）用户认证系统，在 Django 自带的用户系统i的基础上扩展 Oauth 认证，支持微博、Github 等第三方认证
    - [ ] 扩展个人中心界面，设置二级权限，让认证的人能够发送文章。
    - [ ] 支持订阅其他网站的文章信息，统一使用restful api风格。
- [x] App（comment）评论系统，炫酷的输入框特效，支持 markdown 语法，二级评论结构和回复功能
    - [ ] 支持表情包功能，已经增加特效
    - [x] 信息提醒功能，登录和退出提醒，收到评论和回复提醒，信息管理

## 🐾网站开发日志（How to contribute this webproject？）
> 不愿意将这系列的文章叫做教程，感觉这些东西真的网上百度一大堆，希望看到这里的小伙伴们能够意识到合作一起contribute的意识，一起来共同打造更好的项目，👨‍👨‍👦‍👦多人的智慧往往会迸发出更多的火花。

1. 学习使用 markdown 语言来编写文章（basic）
    - [markdown基本语法](https://boywithacoin.cn/article/markdownji-ben-yu-fa/)
2. 克隆 clone 项目后让项目在服务器运行（basic）
    > 大家有问题可以在[网站评论](https://boywithacoin.cn/)或者[github issue](https://github.com/Freen247/django_blog/issues)戳我!
	
    - [Nginx + Gunicorn 服务器配置 Django](https://boywithacoin.cn/article/nginx-gunicorn-fu-wu-qi-pei-zhi-django/)

3. 利用django开发网站日志
    >类似于开发手册/教程，希望可以一起来contribute，支持更多的功能或框架！

    - [django2.0+python3博客基础搭建完成](https://boywithacoin.cn/article/django2-0-python3bo-ke-ji-chu-da-jian-wan-cheng/)
    - [Nginx + Gunicorn 服务器配置 Django](https://boywithacoin.cn/article/nginx-gunicorn-fu-wu-qi-pei-zhi-django/)
    - [django-mdeditor后台内嵌md文章编辑+Editor.md开源项目](https://boywithacoin.cn/article/django-mdeditorhou-tai-nei-qian-mdwen-zhang-bian-ji-editor-mdkai-yuan-xiang-mu/)
    - [django 网站地图 sitemap](https://boywithacoin.cn/article/django-wang-zhan-di-tu-sitemap/)
    - [django的类视图和函数视图](https://boywithacoin.cn/article/djangode-lei-shi-tu-he-han-shu-shi-tu/)，在刚开始建设网站使用的函数视图，后续编写手册时已全部更改为类视图。
    - [django博客开发blog开发日志系统](https://boywithacoin.cn/article/djangobo-ke-kai-fa-blogkai-fa-ri-zhi-xi-tong/)
    - [利用mdeitor配置评论功能、后端利用markdown处理md数据](https://boywithacoin.cn/article/li-yong-mdeitorpei-zhi-ping-lun-gong-neng-hou-duan-li-yong-markdownchu-li-mdshu-ju/)，曾经使用过一段时间，后来改为使用 simplemde 包。
    - [article中上传静态图片时重命名](https://boywithacoin.cn/article/articlezhong-shang-chuan-jing-tai-tu-pian-shi-zhong-ming-ming/)
    - [迁移sqlite3到postgresql数据库](https://boywithacoin.cn/article/qian-yi-sqlite3dao-postgresqlshu-ju-ku)

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

