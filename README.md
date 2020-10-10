# xx

![license](https://img.shields.io/github/license/straycamel247/Django_web)
![repo-size](https://img.shields.io/github/repo-size/straycamel247/Django_web)
![code-size](https://img.shields.io/github/languages/code-size/straycamel247/django_web)

## ✨Features-持续更新

### [🦍Postman接口文档](https://explore.postman.com/templates/12957/djangoweb)

> 开发完后再进行完善

### 👻Version_V2.0

> django+vue，CS系统，集合算法可视化项目，学习、练习、训练模型，系统底层构建等。

- [x] utils: 网站系统功能
  - [x] **创建网站数据类型，用于数据校验**:`apps\types.py`
  - [x] **结合wsme数据校验并扩展自定义数据结构，结合signature装饰器对接口的数据进行数据校验**:`apps\types.py`
  - [x] **自定义signature装饰器，应用于view模板，校验接口传参**:`apps\utils\wsme\signature.py`
  - [x] **自定义彩色日志系统，构建方法打印日志装饰器**:`apps\utils\log\handler.py`
  - [x] **继承rest framework框架的统一的异常处理**:`apps\utils\decorators\http.py`
  - [x] **重构django http请求方式校验，而不是再urls.py文件配置**:`apps\utils\decorators\http.py`
    - [x] 支持将用户指定url和request methods，并将url注册到apis连接下
    - [x] 支持对request.user校验
    - [x] 支持对jwt的token校验（jwt生辰方式见jwt登陆验证），获得token校验后会更新token，将数据插入到返回的json中

- [x] jwt登陆验证
  - [x] 开发简单的jwt登陆验证，绕过drf框架，直接使用django原生系统:`apps\utils\jwt`
  - [x] **登陆接口化，继承rest framework框架登陆路由，扩展使用jwt原理扩展接口**:`apps\accounts\views.py`
    > https://django-rest-framework-simplejwt.readthedocs.io/en/latest/token_types.html#token-types
    - Simple JWT provides two different token types that can be used to prove authentication; 两种方式均可获得对应的token和user信息（user信息使用的序列化功能在`apps\apis\serializers.py`中定制：
    - [x] “access”, “sliding”：`apps\accounts\views.py`:token_obtain_pair()/token_access_refresh()
    - [x] “refresh”：`apps\accounts\views.py`:token_obtain_sliding()/token_refresh()
  - [x] **将django-rest-framework-simplejwt中的CBV视图转换为FBV视图handlers**:`apps\accounts\handler.py`

- [ ] django csrf 接口登陆验证

- [x] apis
  - [x] **获得所有urls**:`apps\apis\views.py`
  
- [x] data
  - [x] **iris_data数据可视化接口**:`apps\data\views.py`

- [x] data_analysis: 使用简单的numpy，pandas复现算法或者模型，并通过接口返回演示
  - [x] **Apriori算法实现**:`apps\data_analysis\models\apriori.py`
  - [x] **FPgrowth算法实现**:`apps\data_analysis\moduls\FPgrowth\handler.py`
  - [x] **SVM算法实现（预测）**:`apps\data_analysis\moduls\svm\handler.py`

- [x] models_sklearn_spark: 机器学习和各种模型算法小demo复现，并通过接口返回演示
  > 开发中...

- [x] models_tensorflow2: 使用tensorflow2复现论文，比赛等，并通过接口返回演示
  > 开发中...

- [x] api: 使用restful framework集成本网站的接口，对外开放，使用RESTful API框架，api主界面在`/api/v1/`
  - [x] 集合用户、博客、工具信息的api。


### [🦄Version_V1.0](https://github.com/StrayCamel247/Django_web/tree/v1.0)

> 网站采用传统的django MVT模式构建，使用bootstrap作为前端框架，用户管理、文章管理、评论系统、留言系统以及工具系统初步完善


<!-- ## 🐾网站

### 项目运行

- 让项目在服务器运行，参考文章：[Nginx + Gunicorn 服务器配置 Django](https://leetcode-cn.com/circle/article/6DA7GA/)
- 服务器可使用`nohup bash gunicorn_start.sh`挂在后台运行。
- 一键清除正在后台运行的config项目，使用命令`bash kill_pid.sh`

- 本地环境运行项目：
    - 安装pip需求包`pip install -r requirements.txt`
    -  更改`settings.py`文件中的数据库配置信息，使用本地`db.sqlite3`文件作数据库。
    - 构建项目所需要的数据库，连接信息更改请在`config/settings.py`文件中进行更改
    - 链接新的数据库或者更换数据库需要运行`python manage.py makemigrations & python manage.py migrate`
    - 集合项目依赖包中的静态文件：`python manage.py collectstatic`
    - 压缩文件:`python manage.py compress`
 -->

### 🙃常见安装项目 bug

- 接口post请求莫名变成get请求:
  - [参考](https://blog.csdn.net/qq_37228688/article/details/89414576)
  - 在url定向的时候，如果末尾不是‘/’，会被系统重定向到带‘/’的url，即301，然后空的请求被重定向，就变成了get
  - 在url末尾加上`/`即可解决。

- `ImportError: PILKit was unable to import the Python Imaging Library. Please confirm it s installe...`
  - 安装pillow库：`pip install pillow`

- `ModuleNotFoundError: No module named 'compressor'`
  - 原因是安装django_compressor时的依赖包rcssm出了问题，重新安装rcssm包
  - `pip install rcssmin --install-option="--without-c-extensions"`

- `ImportError: cannot import name 'connections' from 'haystack' `
  - 常见处理方法；写在自动安装的依赖包`pip uninstall haystack`，如果还不能解决，重新卸载并安装djang-haystack。

- `ImportError: cannot import name 'ChineseAnalyzer' from 'jieba.analyse' `
  - 安装依赖包`whoosh`，其实在requirement里面已经有了，但是估计时没安装成功吧。再安装一次就好了

- `ModuleNotFoundError: No module named 'user_agent'`
  - 这个包直接安装就好，` pip install user_agent`

- 数据库迁移/项目运行bug：`ValueError : unsupported pickle protocol: 5`
  - 这个bug根据pick协议，我们的查询功能whoosh功能时当我们访问这个页面，就将信息缓存下来，由于服务器py版本和win版本不一样可能会导致这个问题，解决方法就是删除项目中`apps\search\whoosh_index`文件夹中的所有文件。


<!-- ### 项目stars曲线图
[![Stargazers over time](https://starcharts.herokuapp.com/StrayCamel247/Django_web.svg)](https://github.com/StrayCamel247/Django_web) -->