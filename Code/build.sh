#!/bin/sh
cd /usr/local/lib
sudo mkdir python3.7
cd python3.7
sudo mkdir dist-packages
cd ~
git clone https://github.com/Freenove/Freenove_RPI_WS281x_Python.git
cd ~/Freenove_RPI_WS281x_Python
sudo python setup.py install
echo "The installation is complete!"
