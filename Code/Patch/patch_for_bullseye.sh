#!/bin/sh
current_file=$0
cd "$(dirname "$current_file")"

#sudo cp /boot/config.txt /boot/config-backup.txt
#sudo cp ./config.txt /boot/config.txt
sudo cp /usr/lib/arm-linux-gnueabihf/libmmal.so /usr/lib/arm-linux-gnueabihf/libmmal-backup.so.backup
sudo cp ./libmmal.so /usr/lib/arm-linux-gnueabihf/libmmal.so

echo "patched complete! Please reboot the system!"

