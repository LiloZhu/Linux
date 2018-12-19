#!/bin/bash

#check process running or not, if no,start it.

PID_NAME='frp'

PIDS=`ps -ef |grep $PID_NAME |grep -v grep | awk '{print $2}'`
echo $PIDS
if [ "$PIDS" != "" ]; then
echo "$PID_NAME is runnig !"
else
echo "------Start $PID_NAME------"
/pisvr01/sh/frp.sh
fi 
