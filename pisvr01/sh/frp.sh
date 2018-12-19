#!/bin/sh -e

echo "------restart frp------"
#pkill -9 frp

/pisvr01/frp/frpc -c /pisvr01/frp/frpc.ini >/dev/null 2>&1  &

echo "------send mail------"

python /pisvr01/program/python/service_mail_msn.py
