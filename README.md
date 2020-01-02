📚 Django 开发的个人网站

🐒 coders：[🐫Stray_camel](https://github.com/Freen247)。
🐾 希望大家一起来合作contribute👍！

**☎ contact me**：
- qq/wechat：1351975058
- email：aboyinsky@outlook.com

## ✨网站功能/计划（Features/future）
> 网站是基于博客系统建立起来的，但是绝对不仅仅局限于这个功能。在这个层面上会更加扩展地开发更多的功能。

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
> 不愿意将这系列的文章叫做教程，感觉这些东西真的网上百度一大堆，希望未来看到这里的小伙伴们能够意识到合作一起contribute的意识，与其自己项目的GitHub星星⭐多，不如一起来fork共同打造更好的项目，👨‍👨‍👦‍👦多人的智慧往往会迸发出更多的火花。

1. 学习使用 markdown 语言来编写文章（basic）
    > md一直是我们程序员常用的记录语言，大家一般使用这种类型的文档来记录或者交流，学了不亏。
	
    - [markdown基本语法](https://boywithacoin.cn/article/markdownji-ben-yu-fa/)
2. 克隆 clone 项目后让项目在服务器或者本地运行（basic）
    > 大家完完全全可以免费使用这款项目，如果想自己开发，玩完全支持。如果大家想学习如何搭建可以跟着我的手册来。大家有问题可以在[网站评论](https://boywithacoin.cn/)或者[github issue](https://github.com/Freen247/django_blog/issues)戳我!
	
    - [Nginx + Gunicorn 服务器配置 Django](https://boywithacoin.cn/article/nginx-gunicorn-fu-wu-qi-pei-zhi-django/)
3. 开发网站项目前的准备
    >大致是一些基础创建django项目和获取/修改前端静态资源的过程，目前涉及到的技术只有bootstrap和css/jq/html/js。希望可以一起来contribute，支持更多的框架！
	
    - [django开发网站-创建django项目](https://boywithacoin.cn/article/djangokai-fa-wang-zhan-chuang-jian-djangoxiang-mu/)
    - [django开发网站-准备并加载静态资源](https://boywithacoin.cn/article/djangokai-fa-wang-zhan-zhun-bei-bing-jia-zai-jing-tai-zi-yuan/)
    - [django开发网站-修改静态资源成博客样式](https://boywithacoin.cn/article/djangokai-fa-wang-zhan-xiu-gai-jing-tai-zi-yuan-cheng-bo-ke-yang-shi/)
    - [django开发网站-（app）user使用第三方登陆](https://boywithacoin.cn/article/djangokai-fa-wang-zhan-app-usershi-yong-di-san-fang-deng-lu/)
    - [django开发网站-添加博客系统(app)](https://boywithacoin.cn/article/djangokai-fa-wang-zhan-tian-jia-bo-ke-xi-tong-app/)
    - [django开发网站-评论系统](https://boywithacoin.cn/article/djangokai-fa-wang-zhan-ping-lun-xi-tong/)
    - ...文章编写中ing
    - [django2.0+python3博客基础搭建完成](https://boywithacoin.cn/article/django2-0-python3bo-ke-ji-chu-da-jian-wan-cheng/)
    - [Nginx + Gunicorn 服务器配置 Django](https://boywithacoin.cn/article/nginx-gunicorn-fu-wu-qi-pei-zhi-django/)
    - [django-mdeditor后台内嵌md文章编辑+Editor.md开源项目](https://boywithacoin.cn/article/django-mdeditorhou-tai-nei-qian-mdwen-zhang-bian-ji-editor-mdkai-yuan-xiang-mu/)
    - [django 网站地图 sitemap](https://boywithacoin.cn/article/django-wang-zhan-di-tu-sitemap/)
    - [django的类视图和函数视图](https://boywithacoin.cn/article/djangode-lei-shi-tu-he-han-shu-shi-tu/)，在刚开始建设网站使用的函数视图，后续编写手册时已全部更改为类视图。
    - [django博客开发blog开发日志系统](https://boywithacoin.cn/article/djangobo-ke-kai-fa-blogkai-fa-ri-zhi-xi-tong/)
    - [利用mdeitor配置评论功能、后端利用markdown处理md数据](https://boywithacoin.cn/article/li-yong-mdeitorpei-zhi-ping-lun-gong-neng-hou-duan-li-yong-markdownchu-li-mdshu-ju/)，曾经使用过一段时间，后来改为使用 simplemde 包。
    - [article中上传静态图片时重命名](https://boywithacoin.cn/article/articlezhong-shang-chuan-jing-tai-tu-pian-shi-zhong-ming-ming/)
    - [django开发网站-迁移sqlite3数据库到postgresql数据库](https://boywithacoin.cn/article/djangokai-fa-wang-zhan-qian-yi-sqlite3shu-ju-ku-dao-postgresqlshu-ju-ku/)
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

    
## 🐒网站实际效果预览
![Python](https://camo.githubusercontent.com/42a16d3ced93f9da9842bd59c778c4cffca16e11/68747470733a2f2f63646e2e6c6561726e6b752e636f6d2f75706c6f6164732f696d616765732f3230323030312f30322f32323839332f52564a46524d4f5135432e706e67216c61726765)

![](https://camo.githubusercontent.com/9f3fbd8ada0611b65b6edda1bfb3e4851e7e9a30/68747470733a2f2f626f797769746861636f696e2e636e2f7374617469632f6d656469612f656469746f722f54494d25453625383825414125453525394225424532303230303130313232333632315f32303230303130313232333730353239303239362e706e67)
