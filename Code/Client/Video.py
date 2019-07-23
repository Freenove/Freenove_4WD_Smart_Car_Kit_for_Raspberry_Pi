#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import io
import sys
from PIL import Image
from multiprocessing import Process
from Command import COMMAND as cmd

#socket.setdefaulttimeout(5)  #new
class VideoStreaming:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        self.video_Flag=True
        self.connect_Flag=False #new
    def StartTcpClient(self,IP):
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'StartTcpClient'
    def StopTcpcClient(self):
        try:
            self.connection.close()
            self.client_socket.close()
            self.client_socket1.close()
        except:
            pass
    
    def IsValidImage4Bytes(self,buf): 
        bValid = True
        if buf[6:10] in (b'JFIF', b'Exif'):     
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                bValid = False
        else:        
            try:  
                Image.open(io.BytesIO(buf)).verify() 
            except:  
                bValid = False
         
        return bValid

    def face_detect(self,img):
        if sys.platform.startswith('win'):
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray,1.3,5)
            if len(faces)>0 :
                for (x,y,w,h) in faces:
                    img = cv2.circle(img, (x+w/2,y+h/2), (w+h)/4, (0, 255, 0), 2)
        else:
            pass
        cv2.imwrite('video.jpg', img)
        
    def streaming(self,ip):
        try:
            stream_bytes = b' '
            self.client_socket.connect((ip, 8000))
            self.connection = self.client_socket.makefile('wb')
            while True:
                try:
                    stream_bytes += self.connection.read(1024)
                    first = stream_bytes.find(b'\xff\xd8')
                    last = stream_bytes.find(b'\xff\xd9')
                    if first != -1 and last != -1 :      
                        jpg = stream_bytes[first:last + 2]
                        stream_bytes = stream_bytes[last + 2:]
                        if self.IsValidImage4Bytes(jpg):
                            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                            if self.video_Flag:
                                self.face_detect(image)
                except:
                    break
        except:
            pass
                    
    def sendData(self,s):
        if self.connect_Flag:
            self.client_socket1.send(s)
        else:
            pass

    def recvData(self):
        data=0
        try:
            data=self.client_socket1.recv(1024)
        except:
            pass
        return data

    def socket1_connect(self,ip):
        try:
            self.client_socket1.connect((ip, 5000))
            self.connect_Flag=True
            print "Connecttion Successful !"
        except Exception, e:
            print "Connect to server Faild!: Server IP is right? Server is opend?", e
            self.connect_Flag=False

if __name__ == '__main__':
    a=VideoStreaming()
    pass

