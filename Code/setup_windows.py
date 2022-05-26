import os
import sys
import time
flag=0x00
for x in range(1,4):
	if os.system("python -m pip install --upgrade pip --user") == 0:
		flag=flag | 0x01
		break
for x in range(1,4):
	if os.system("pip3 install PyQt5") == 0:
		flag=flag | 0x02
		break
for x in range(1,4):
	if os.system("pip3 install Pillow") == 0:
		flag=flag | 0x04
		break
for x in range(1,4):
	if os.system("pip3 install opencv-python") == 0:
		if os.system("pip3 install opencv-contrib-python") == 0:
			flag=flag | 0x08
			break
for x in range(1,4):
	if os.system("pip3 install numpy") == 0:
		flag=flag | 0x10
		break
if flag==0x1f:
		os.system("pip3 list && pause")
		print("\nAll libraries installed successfully")
else:
		print ("\nSome libraries have not been installed yet. Please run 'sudo python setup_windows.py' again")

	
	


