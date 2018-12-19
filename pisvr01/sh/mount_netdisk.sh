#!/bin/sh -e

echo "------Mount NetDisk Size: 150 GB------"
#mount /dev/sda1 /mnt/netdisk
mount -t ntfs -o uid=0,gid=0,umask=000 UUID="26061E07061DD91F" /mnt/netdisk