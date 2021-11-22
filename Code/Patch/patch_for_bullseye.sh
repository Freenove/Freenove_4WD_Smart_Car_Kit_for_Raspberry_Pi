#!/bin/sh
current_file=$0
cd "$(dirname "$current_file")"

#sudo cp /boot/config.txt /boot/config-backup.txt
#sudo cp ./config.txt /boot/config.txt

sudo cp /usr/lib/arm-linux-gnueabihf/libmmal.so /usr/lib/arm-linux-gnueabihf/libmmal-backup.so.backup
sudo cp ./libmmal.so /usr/lib/arm-linux-gnueabihf/libmmal.so

sudo cp /opt/vc/lib/libmmal.so /opt/vc/lib/libmmal.so.bak 
sudo cp ./libmmal.so /opt/vc/lib/libmmal.so

echo "patched complete!"

