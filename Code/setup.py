import os
import sys
import time
os.system("cd /usr/bin && sudo rm python && sudo ln -s python3 python")
flag=0x00
for x in range(1,4):
    if os.system("sudo apt-get update") == 0:
        flag=flag | 0x01
        break
for x in range(1,4):
    if os.system("sudo apt-get install -y python3-dev python3-pyqt5 ") == 0:
        flag=flag | 0x02
        break
if flag==0x03:
    print("\nNow the installation is successful.")
else:
    print ("\nSome libraries have not been installed yet. Please run 'sudo python setup.py' again")

