import os
# 项目环境变量

"""
项目启动前若不适用默认文件，则需要配置此环境变量
>>> import os
>>> os.environ['django_web_flag'] = 'dev'
>>> env = os.getenv('django_web_env', 'loc')
"""
env = os.getenv('django_web_env', 'loc')
