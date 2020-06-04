#! /bin/bash
# process-monitor.sh
pid=$(ps -ef | grep gunicorn  | grep -v grep | awk '{print $2}')
echo $pid
# start with a try
kill -9 $pid
