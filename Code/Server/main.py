import io
import os
import socket
import struct
import time
import picamera
import sys,getopt
from threading import Thread
from server_ui import Ui_server_ui
from PyQt4.QtCore import *
from Thread import *
from PyQt4 import  QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import (QApplication, QMainWindow, QGraphicsScene)
from server import video

class mywindow(QMainWindow,Ui_server_ui):
    
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.user_ui=True
        self.m_DragPosition=self.pos()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.Button_Server.setText("On")
        self.Button_Server.clicked.connect(self.on_pushButton)
        self.pushButton_Close.clicked.connect(self.close)
        self.pushButton_Min.clicked.connect(self.windowMinimumed)
        self.myvideo=video()
        self.SendVideo=Thread(target=self.myvideo.sendvideo)
        self.ReadData=Thread(target=self.myvideo.readdata)
        self.parseOpt()
    def windowMinimumed(self):
        self.showMinimized()
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
 
    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
 
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        
    def parseOpt(self):
        self.opts,self.args = getopt.getopt(sys.argv[1:],"tn")
        for o,a in self.opts:
            if o in ('-t'):
                print "Open TCP"
                self.myvideo.StartTcpServer()
                self.ReadData=Thread(target=self.myvideo.readdata)
                self.SendVideo=Thread(target=self.myvideo.sendvideo)
                self.SendVideo.start()
                self.ReadData.start()
                
                self.label.setText("Server On")
                self.Button_Server.setText("Off")
            elif o in ('-n'):
                self.user_ui=False
                        
    def close(self):
        try:
           stop_thread(self.SendVideo)
           stop_thread(self.ReadData)
        except:
            pass
        try:
            self.myvideo.server_socket.shutdown(2)
            self.myvideo.server_socket1.shutdown(2)
            self.myvideo.StopTcpServer()
        except:
            pass
        print "Close Server"
        QCoreApplication.instance().quit()
        os._exit(0)
    def on_pushButton(self):
        if self.label.text()=="Server Off":
            self.label.setText("Server On")
            self.Button_Server.setText("Off")
            self.myvideo.StartTcpServer()
            self.SendVideo=Thread(target=self.myvideo.sendvideo)
            self.ReadData=Thread(target=self.myvideo.readdata)
            self.SendVideo.start()
            self.ReadData.start()
            print "Open TCP"
        elif self.label.text()=='Server On':
            self.label.setText("Server Off")
            self.Button_Server.setText("On")
            try:
                time.sleep(0.1)
                stop_thread(self.SendVideo)
                stop_thread(self.ReadData)
            except:
                print 'stop_thread error'
            
            self.myvideo.StopTcpServer()
            print "Close TCP"
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow=mywindow()
    if myshow.user_ui==True:
        myshow.show();   
        sys.exit(app.exec_())
    else:
        try:
            while(1):
                pass
        except KeyboardInterrupt:
            myshow.close()
            

                    
    


