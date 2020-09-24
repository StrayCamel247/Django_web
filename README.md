📚 Django 可视化项目

🐒 coders：[🐫Stray_camel](https://github.com/StrayCamel247)

**☎ 联系方式**：
- prefer：[github/issue](https://github.com/StrayCamel247/Django_web/issues)
- email：aboyinsky@outlook.com/wechat：1351975058

## ✨网站/规划功能/计划（Features/future）-持续更新...
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


### Version_1.0
> 集成用户管理，文章博客管理，评论系统，mvt模式，bootstrap前端网站，学习django上手的项目，此项目的初始版本。
[跳转到v1.0](https://github.com/StrayCamel247/Django_web/tree/v1.0)


