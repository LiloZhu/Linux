#!/bin/sh -e

echo "------Start SSH------"
/etc/init.d/ssh restart
#echo "------Start VNC------"
#sudo vncserver :1
#echo "------Mount NetDisk Size: 150 GB------"
#mount /dev/sda1 /mnt/netdisk
#mount -t ntfs -o uid=0,gid=0,umask=000 UUID="26061E07061DD91F" /mnt/netdisk
#echo "------Mount NetCloud Size: 4 TB------"
#mount UUID="F670994A7099130B" /mnt/netcloud

echo "------Start Nginx------"
service nginx restart

#echo "------Start Thunder------"
#sudo /software/thunder/portal

echo "------Start samba------"
/etc/init.d/samba restart

echo "------Start minidlna------"
/etc/init.d/minidlna restart

#echo "------Start aria2------"
#sudo aria2c --conf-path=/etc/aria2/aria2.conf -D

