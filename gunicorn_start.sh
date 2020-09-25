#!/bin/bash
NAME='django_blog' #应用的名称i
DJANGODIR=/home/django_blog #django项目的目录
SOCKFILE=/home/django_blog/gunicorn.sock #使用这个sock来通信
USER=root #运行此应用的用户
GROUP=root #运行此应用的组
NUM_WORKERS=3 #gunicorn使用的工作进程数
DJANGO_SETTINGS_MODULE=django_blog.settings #django的配置文件
DJANGO_WSGI_MODULE=django_blog.wsgi #wsgi模块
LOG_DIR=/home/logs #日志目录
echo "starting $NAME as `whoami`"
#激活python虚拟运行环境
cd /home/
source env/bin/activate
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
#如果gunicorn.sock所在目录不存在则创建
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
#启动Django
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --log-level=debug \
    --bind=unix:$SOCKFILE \
    --access-logfile=${LOG_DIR}/gunicorn_access.log
