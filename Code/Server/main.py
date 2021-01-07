import io
import os
import socket
import struct
import time
import picamera
import sys,getopt
from Thread import *
from threading import Thread
from server import Server
from server_ui import Ui_server_ui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class mywindow(QMainWindow,Ui_server_ui):
    
    def __init__(self):
        self.user_ui=True
        self.start_tcp=False
        self.TCP_Server=Server()
        self.parseOpt()
        if self.user_ui:
            self.app = QApplication(sys.argv)
            super(mywindow,self).__init__()
            self.setupUi(self)
            self.m_DragPosition=self.pos()
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setMouseTracking(True)
            self.Button_Server.setText("On")
            self.on_pushButton()
            self.Button_Server.clicked.connect(self.on_pushButton)
            self.pushButton_Close.clicked.connect(self.close)
            self.pushButton_Min.clicked.connect(self.windowMinimumed)
        
        if self.start_tcp:
            self.TCP_Server.StartTcpServer()
            self.ReadData=Thread(target=self.TCP_Server.readdata)
            self.SendVideo=Thread(target=self.TCP_Server.sendvideo)
            self.power=Thread(target=self.TCP_Server.Power)
            self.SendVideo.start()
            self.ReadData.start()
            self.power.start()
            if self.user_ui:
                self.label.setText("Server On")
                self.Button_Server.setText("Off")
                
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
                print ("Open TCP")
                self.start_tcp=True
            elif o in ('-n'):
                self.user_ui=False
                        
    def close(self):
        try:
           stop_thread(self.SendVideo)
           stop_thread(self.ReadData)
           stop_thread(self.power)
        except:
            pass
        try:
            self.TCP_Server.server_socket.shutdown(2)
            self.TCP_Server.server_socket1.shutdown(2)
            self.TCP_Server.StopTcpServer()
        except:
            pass
        print ("Close TCP")
        if self.user_ui:
            QCoreApplication.instance().quit()
        os._exit(0)
    def on_pushButton(self):
        if self.label.text()=="Server Off":
            self.label.setText("Server On")
            self.Button_Server.setText("Off")
            self.TCP_Server.tcp_Flag = True
            print ("Open TCP")
            self.TCP_Server.StartTcpServer()
            self.SendVideo=Thread(target=self.TCP_Server.sendvideo)
            self.ReadData=Thread(target=self.TCP_Server.readdata)
            self.power=Thread(target=self.TCP_Server.Power)
            self.SendVideo.start()
            self.ReadData.start()
            self.power.start()
            
        elif self.label.text()=='Server On':
            self.label.setText("Server Off")
            self.Button_Server.setText("On")
            self.TCP_Server.tcp_Flag = False
            try:
                stop_thread(self.ReadData)
                stop_thread(self.power)
                stop_thread(self.SendVideo)
            except:
                pass
            self.TCP_Server.StopTcpServer()
            print ("Close TCP")
            
if __name__ == '__main__':
    myshow=mywindow()
    if myshow.user_ui==True:
        myshow.show();   
        sys.exit(myshow.app.exec_())
    else:
        try:
            pass
        except KeyboardInterrupt:
            myshow.close()
