#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import os
import io
import time
import imghdr
import sys
from threading import Timer
from threading import Thread
from PIL import Image
from Command import COMMAND as cmd
from Thread import *
from Client_Ui import Ui_Client
from Video import *
from PyQt4.QtCore import *
from PyQt4 import  QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import (QApplication, QMainWindow, QGraphicsScene)


        
class mywindow(QMainWindow,Ui_Client):
    def __init__(self):
        global timer
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.h=self.IP.text()
        self.TCP=VideoStreaming()
        self.servo1=90
        self.servo2=20
        self.label_FineServo2.setText("0")
        self.label_FineServo1.setText("0")
        self.m_DragPosition=self.pos()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.Key_W=False
        self.Key_A=False
        self.Key_S=False
        self.Key_D=False
        self.Key_Space=False
        
        self.setFocusPolicy(Qt.StrongFocus)

        self.progress_Power.setMinimum(0)
        self.progress_Power.setMaximum(100)
        
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Servo1.setText('90')
        self.label_Servo2.setText('20')
        self.label_Video.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.label_Servo1.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.label_Servo2.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        
        self.label_FineServo1.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.label_FineServo2.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        
        

        self.HSlider_Servo1.setMinimum(0)
        self.HSlider_Servo1.setMaximum(180)
        self.HSlider_Servo1.setSingleStep(1)
        self.HSlider_Servo1.setValue(self.servo1)
        self.HSlider_Servo1.valueChanged.connect(self.Change_Left_Right)

        self.HSlider_FineServo1.setMinimum(-10)
        self.HSlider_FineServo1.setMaximum(10)
        self.HSlider_FineServo1.setSingleStep(1)
        self.HSlider_FineServo1.setValue(0)
        self.HSlider_FineServo1.valueChanged.connect(self.Fine_Tune_Left_Right)

        self.HSlider_FineServo2.setMinimum(-10)
        self.HSlider_FineServo2.setMaximum(10)
        self.HSlider_FineServo2.setSingleStep(1)
        self.HSlider_FineServo2.setValue(0)
        self.HSlider_FineServo2.valueChanged.connect(self.Fine_Tune_Up_Down)
        
        self.VSlider_Servo2.setMinimum(0)
        self.VSlider_Servo2.setMaximum(150)
        self.VSlider_Servo2.setSingleStep(1)
        self.VSlider_Servo2.setValue(self.servo2)
        self.VSlider_Servo2.valueChanged.connect(self.Change_Up_Down)
        
        self.checkBox_Led1.setChecked(False)
        self.checkBox_Led1.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led1))
        self.checkBox_Led2.setChecked(False)
        self.checkBox_Led2.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led2))
        self.checkBox_Led3.setChecked(False)
        self.checkBox_Led3.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led3))
        self.checkBox_Led4.setChecked(False)
        self.checkBox_Led4.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led4))
        self.checkBox_Led5.setChecked(False)
        self.checkBox_Led5.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led5))
        self.checkBox_Led6.setChecked(False)
        self.checkBox_Led6.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led6))
        self.checkBox_Led7.setChecked(False)
        self.checkBox_Led7.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led7))
        self.checkBox_Led8.setChecked(False)
        self.checkBox_Led8.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led8))
        
        self.checkBox_Led_Mode1.setChecked(False)
        self.checkBox_Led_Mode1.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led_Mode1))
        self.checkBox_Led_Mode2.setChecked(False)
        self.checkBox_Led_Mode2.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led_Mode2))
        self.checkBox_Led_Mode3.setChecked(False)
        self.checkBox_Led_Mode3.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led_Mode3))
        self.checkBox_Led_Mode4.setChecked(False)
        self.checkBox_Led_Mode4.stateChanged.connect(lambda:self.LedChange(self.checkBox_Led_Mode4)) 

        self.Btn_Mode1.setChecked(True)
        self.Btn_Mode1.toggled.connect(lambda:self.on_btn_Mode(self.Btn_Mode1))
        self.Btn_Mode2.setChecked(False)
        self.Btn_Mode2.toggled.connect(lambda:self.on_btn_Mode(self.Btn_Mode2))
        self.Btn_Mode3.setChecked(False)
        self.Btn_Mode3.toggled.connect(lambda:self.on_btn_Mode(self.Btn_Mode3))
        self.Btn_Mode4.setChecked(False)
        self.Btn_Mode4.toggled.connect(lambda:self.on_btn_Mode(self.Btn_Mode4))
        
        self.Ultrasonic.clicked.connect(self.on_btn_Ultrasonic)
        self.Light.clicked.connect(self.on_btn_Light)
        
        self.Btn_ForWard.pressed.connect(self.on_btn_ForWard)
        self.Btn_ForWard.released.connect(self.on_btn_Stop)

        self.Btn_Turn_Left.pressed.connect(self.on_btn_Turn_Left)
        self.Btn_Turn_Left.released.connect(self.on_btn_Stop)

        self.Btn_BackWard.pressed.connect(self.on_btn_BackWard)
        self.Btn_BackWard.released.connect(self.on_btn_Stop)

        self.Btn_Turn_Right.pressed.connect(self.on_btn_Turn_Right)
        self.Btn_Turn_Right.released.connect(self.on_btn_Stop)

        self.Btn_Video.clicked.connect(self.on_btn_video)

        self.Btn_Up.clicked.connect(self.on_btn_Up)
        self.Btn_Left.clicked.connect(self.on_btn_Left)
        self.Btn_Down.clicked.connect(self.on_btn_Down)
        self.Btn_Home.clicked.connect(self.on_btn_Home)
        self.Btn_Right.clicked.connect(self.on_btn_Right)

        self.Btn_Buzzer.pressed.connect(self.on_btn_Buzzer)
        self.Btn_Buzzer.released.connect(self.on_btn_Buzzer)
        
        self.Btn_Connect.clicked.connect(self.on_btn_Connect)
        
        
        self.Window_Min.clicked.connect(self.windowMinimumed)
        self.Window_Close.clicked.connect(self.close)
        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.time)
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
    def close(self):
        timer.stop()
        try:
            self.TCP.sendData(cmd.CMD_POWER_OFF)
            self.TCP.sendData(cmd.CMD_CLOSE)
            stop_thread(self.streaming)
            stop_thread(self.recv)
            self.TCP.StopTcpcClient()
        except:
            pass
        try:
            os.remove("video.jpg")
        except:
            pass
        QCoreApplication.instance().quit()
        os._exit(0)
        
    def recvmassage(self):
        self.receflag=1
        try:
            self.TCP.socket1_connect(self.h)
            self.TCP.sendData(cmd.CMD_POWER_ON)
            while True:
                Alldata=self.TCP.recvData()
                if Alldata==None:
                    pass
                elif Alldata=='':
                    break
                elif len(Alldata)>21:
                    continue
                else :
                    Massage=Alldata.split("#")
                if cmd.CMD_SONIC in Massage:
                    self.Ultrasonic.setText('Obstruction:%s cm'%Massage[1])
                elif cmd.CMD_SERVO in Massage:
                    print Massage
                elif cmd.CMD_LIGHT in Massage:
                    self.Light.setText("Left:"+Massage[1]+'V'+' '+"Right"+Massage[2]+'V')
                elif cmd. CMD_POWER in Massage:
                    percent_power=int((float(Massage[1])*3-7)/1.40*100)
                    self.progress_Power.setValue(percent_power)
                else:
                    pass
        except :
            pass
        
    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Up):
            self.on_btn_Up()
        elif(event.key() == Qt.Key_Left):
            self.on_btn_Left()
        elif(event.key() == Qt.Key_Down):
            self.on_btn_Down()
        elif(event.key() == Qt.Key_Right):
            self.on_btn_Right()
        elif(event.key() == Qt.Key_Home):
            self.on_btn_Home()


        if(event.key() == Qt.Key_Q):
            if self.Btn_Mode1.isChecked() == True:
                self.Btn_Mode2.setChecked(True)
            elif self.Btn_Mode2.isChecked() == True:
                self.Btn_Mode3.setChecked(True)
            elif self.Btn_Mode3.isChecked() == True:
                self.Btn_Mode4.setChecked(True)
            elif self.Btn_Mode4.isChecked() == True:
                self.Btn_Mode1.setChecked(True)

        if(event.key() == Qt.Key_L):
            count=0
            if  self.checkBox_Led_Mode1.isChecked() == True:
                self.checkBox_Led_Mode2.setChecked(True)
            elif  self.checkBox_Led_Mode2.isChecked() == True:
                self.checkBox_Led_Mode3.setChecked(True)
            elif  self.checkBox_Led_Mode3.isChecked() == True:
                self.checkBox_Led_Mode4.setChecked(True)
            elif  self.checkBox_Led_Mode4.isChecked() == True:
                self.checkBox_Led_Mode1.setChecked(True)

            for i in range(1,5):
                checkBox_Led_Mode=getattr(self,"checkBox_Led_Mode%d"%i)
                if  checkBox_Led_Mode.isChecked() == False:
                    count+=1
                else:
                    break
            if count ==4:
                self.checkBox_Led_Mode1.setChecked(True)
                
        if(event.key() == Qt.Key_C):
            self.on_btn_Connect()
        if(event.key() == Qt.Key_V):
            self.on_btn_video()

            
        if(event.key() == Qt.Key_1):
            if self.checkBox_Led1.isChecked() == True:
                self.checkBox_Led1.setChecked(False)
            else:
                self.checkBox_Led1.setChecked(True)
        elif(event.key() == Qt.Key_2):
            if self.checkBox_Led2.isChecked() == True:
                self.checkBox_Led2.setChecked(False)
            else:
                self.checkBox_Led2.setChecked(True)
        elif(event.key() == Qt.Key_3):
            if self.checkBox_Led3.isChecked() == True:
                self.checkBox_Led3.setChecked(False)
            else:
                self.checkBox_Led3.setChecked(True)
        elif(event.key() == Qt.Key_4):
            if self.checkBox_Led4.isChecked() == True:
                self.checkBox_Led4.setChecked(False)
            else:
                self.checkBox_Led4.setChecked(True)
        elif(event.key() == Qt.Key_5):
            if self.checkBox_Led5.isChecked() == True:
                self.checkBox_Led5.setChecked(False)
            else:
                self.checkBox_Led5.setChecked(True)
        elif(event.key() == Qt.Key_6):
            if self.checkBox_Led6.isChecked() == True:
                self.checkBox_Led6.setChecked(False)
            else:
                self.checkBox_Led6.setChecked(True)
        elif(event.key() == Qt.Key_7):
            if self.checkBox_Led7.isChecked() == True:
                self.checkBox_Led7.setChecked(False)
            else:
                self.checkBox_Led7.setChecked(True)
        elif(event.key() == Qt.Key_8):
            if self.checkBox_Led8.isChecked() == True:
                self.checkBox_Led8.setChecked(False)
            else:
                self.checkBox_Led8.setChecked(True)

                
        if event.isAutoRepeat():
            pass
        else :
            #print "You Pressed Key : ", event.key(), event.text() 
            if event.key() == Qt.Key_W:
                self.on_btn_ForWard()
                self.Key_W=True
            elif event.key() == Qt.Key_S:
                self.on_btn_BackWard()
                self.Key_S=True
            elif event.key() == Qt.Key_A:
                self.on_btn_Turn_Left()
                self.Key_A=True
            elif event.key() == Qt.Key_D:                  
                self.on_btn_Turn_Right()
                self.Key_D=True  
            elif event.key() == Qt.Key_Space:  
                self.on_btn_Buzzer()
                self.Key_Space=True                

    def keyReleaseEvent(self, event):

        if(event.key() == Qt.Key_W):
            time.sleep(0.05)
            if(event.key() == Qt.Key_W):
                if not(event.isAutoRepeat()) and self.Key_W==True:
                    self.on_btn_Stop()
                    self.Key_W=False
        elif(event.key() == Qt.Key_A):
            if not(event.isAutoRepeat()) and self.Key_A==True:
                self.on_btn_Stop()
                self.Key_A=False
        elif(event.key() == Qt.Key_S):
            if not(event.isAutoRepeat()) and self.Key_S==True:
                self.on_btn_Stop()
                self.Key_S=False
        elif(event.key() == Qt.Key_D):
            if not(event.isAutoRepeat()) and self.Key_D==True:
                self.on_btn_Stop()
                self.Key_D=False
                
        if(event.key() == Qt.Key_Space):
            if not(event.isAutoRepeat()) and self.Key_Space==True:
                self.on_btn_Buzzer()
                self.Key_Space=False
        

        
    def on_btn_ForWard(self):
        self.TCP.sendData(cmd.CMD_FORWARD)

    def on_btn_Turn_Left(self):
        self.TCP.sendData(cmd.CMD_TURULEFT)

    def on_btn_BackWard(self):
        self.TCP.sendData(cmd.CMD_BACKWARD)

    def on_btn_Turn_Right(self):
        self.TCP.sendData(cmd.CMD_TURNRIGHT)

    def on_btn_Stop(self):
        self.TCP.sendData(cmd.CMD_MOTORSTOP)

    def on_btn_video(self):
        if self.Btn_Video.text()=='Open Video':
            timer.start(34)
            self.Btn_Video.setText('Close Video')
        elif self.Btn_Video.text()=='Close Video':
            timer.stop()
            self.Btn_Video.setText('Open Video')
    def on_btn_Up(self):
        self.servo2=self.servo2+10
        if self.servo2>=150:
            self.servo2=150
        self.VSlider_Servo2.setValue(self.servo2)
        self.TCP.sendData(cmd.CMD_SERVO2+str(self.servo2))

        self.label_Servo2.setText("%d"%self.servo2)
    def on_btn_Left(self):
        self.servo1=self.servo1-10
        if self.servo1<=0:
            self.servo1=0
        self.HSlider_Servo1.setValue(self.servo1)
        self.TCP.sendData(cmd.CMD_SERVO1+str(self.servo1)+'#0')

        self.label_Servo1.setText("%d"%self.servo1)
    def on_btn_Down(self):
        self.servo2=self.servo2-10
        if self.servo2<=0:
            self.servo2=0
        self.VSlider_Servo2.setValue(self.servo2)
        self.TCP.sendData(cmd.CMD_SERVO2+str(self.servo2))

        self.label_Servo2.setText("%d"%self.servo2)

    def on_btn_Home(self):
        self.servo1=90
        self.servo2=20
        self.HSlider_Servo1.setValue(self.servo1)
        self.label_Servo1.setText("%d"%self.servo1)
        self.VSlider_Servo2.setValue(self.servo2)
        self.label_Servo2.setText("%d"%self.servo2)

    def on_btn_Right(self):
        self.servo1=self.servo1+10
        if self.servo1>=180:
            self.servo1=180
        self.HSlider_Servo1.setValue(self.servo1)
        self.TCP.sendData(cmd.CMD_SERVO1+str(self.servo1)+'#0')

        self.label_Servo1.setText("%d"%self.servo1)

        
    def Change_Left_Right(self):#Left or Right
        self.servo1=self.HSlider_Servo1.value()
        self.TCP.sendData(cmd.CMD_SERVO1+str(self.servo1)+'#0')
        self.label_Servo1.setText("%d"%self.servo1)
        
    def Fine_Tune_Left_Right(self):#fine tune Left or Right
        self.label_FineServo1.setText(str(self.HSlider_FineServo1.value()))
        data=self.servo1+self.HSlider_FineServo1.value()
        self.TCP.sendData(cmd.CMD_SERVO1+str(data)+'#0')

    def Fine_Tune_Up_Down(self):#fine tune Up or Down
        self.label_FineServo2.setText(str(self.HSlider_FineServo2.value()))
        data=self.servo2+self.HSlider_FineServo2.value()
        self.TCP.sendData(cmd.CMD_SERVO2+str(data))

        
    def Change_Up_Down(self):#Up or Down
        self.servo2=self.VSlider_Servo2.value()
        self.TCP.sendData(cmd.CMD_SERVO2+str(self.servo2))
        self.label_Servo2.setText("%d"%self.servo2)

    def windowMinimumed(self):
        self.showMinimized()


    def on_btn_Buzzer(self):
        if self.Btn_Buzzer.text()=='Buzzer':
            self.TCP.sendData(cmd.CMD_BUZZER_ON)
            self.Btn_Buzzer.setText('Noise')
        else:
            self.TCP.sendData(cmd.CMD_BUZZER_OFF)
            self.Btn_Buzzer.setText('Buzzer')

    def LedChange(self,b):
        R=self.Color_R.text()
        G=self.Color_G.text()
        B=self.Color_B.text()
        if b.text() == "Led1":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED2_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED2_OFF)
        if b.text() == "Led2":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED3_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED3_OFF)               
        if b.text() == "Led3":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED4_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED4_OFF)
        if b.text() == "Led4":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED5_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED5_OFF)
        if b.text() == "Led5":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED1_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED1_OFF)
        if b.text() == "Led6":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED0_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED0_OFF)
        if b.text() == "Led7":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED7_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED7_OFF)
        if b.text() == "Led8":
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED6_ON+str(R)+"#"+str(G)+"#"+str(B))
           else:
               self.TCP.sendData(cmd.CMD_LED6_OFF)
        if b.text() == "Led_Mode1":
           if b.isChecked() == True:
               self.checkBox_Led_Mode2.setChecked(False)
               self.checkBox_Led_Mode3.setChecked(False)
               self.checkBox_Led_Mode4.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD1)
           else:
               self.TCP.sendData(cmd.CMD_LED_OFF)
        if b.text() == "Led_Mode2":
           if b.isChecked() == True:

               self.checkBox_Led_Mode1.setChecked(False)
               self.checkBox_Led_Mode3.setChecked(False)
               self.checkBox_Led_Mode4.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD2)
           else:
               self.TCP.sendData(cmd.CMD_LED_OFF)
        if b.text() == "Led_Mode3":
           if b.isChecked() == True:
               self.checkBox_Led_Mode2.setChecked(False)
               self.checkBox_Led_Mode1.setChecked(False)
               self.checkBox_Led_Mode4.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD3)
           else:
               self.TCP.sendData(cmd.CMD_LED_OFF)
        if b.text() == "Led_Mode4":
           if b.isChecked() == True:
               self.checkBox_Led_Mode2.setChecked(False)
               self.checkBox_Led_Mode3.setChecked(False)
               self.checkBox_Led_Mode1.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD4)
           else:
               self.TCP.sendData(cmd.CMD_LED_OFF)
    def on_btn_Ultrasonic(self):
        if self.Ultrasonic.text()=="Ultrasonic":
            self.TCP.sendData(cmd.CMD_ULTRASONIC_ON)
        else:
            self.TCP.sendData(cmd.CMD_ULTRASONIC_OFF)
            self.Ultrasonic.setText("Ultrasonic")
 
    def on_btn_Light(self):
        if self.Light.text() == "Light":
            self.TCP.sendData(cmd.CMD_LIGHT_ON)
        else:
            self.TCP.sendData(cmd.CMD_LIGHT_OFF)
            self.Light.setText("Light")
 
    def on_btn_Mode(self,Mode):
        if Mode.text() == "M-Free":
            if Mode.isChecked() == True:
                timer.start(34)
                self.TCP.sendData(cmd.CMD_MODE[0])
                
        if Mode.text() == "M-Light":
            if Mode.isChecked() == True:
                timer.stop()
                self.TCP.sendData(cmd.CMD_MODE[1])
        if Mode.text() == "M-Sonic":
            if Mode.isChecked() == True:
                timer.stop()
                self.TCP.sendData(cmd.CMD_MODE[2])
                
        if Mode.text() == "M-Line":
            if Mode.isChecked() == True:
                timer.stop()
                self.TCP.sendData(cmd.CMD_MODE[3])
         
                                  
    def on_btn_Connect(self):
        if self.Btn_Connect.text() == "Connect":
            self.h=self.IP.text()
            self.TCP.StartTcpClient(self.h,)
            try:
                self.streaming=Thread(target=self.TCP.streaming,args=(self.h,))
                self.streaming.start()
            except:
                print 'video error'
            try:
                self.recv=Thread(target=self.recvmassage)
                self.recv.start()
            except:
                print 'recv error'
            self.Btn_Connect.setText( "Disconnect")
            print (self.h)
        elif self.Btn_Connect.text()=="Disconnect":
            self.Btn_Connect.setText( "Connect")
            self.TCP.windows=0
            self.receflag=0
            try:
                stop_thread(self.streaming)
                stop_thread(self.recv)
                self.TCP.sendData(cmd.CMD_POWER_OFF)
                self.TCP.client_socket1.send(cmd.CMD_CLOSE)
                self.TCP.StopTcpcClient()
            except:
                pass

         
    def is_valid_jpg(self,jpg_file):
        try:
            
            if jpg_file.split('.')[-1].lower() == 'jpg':  
                with open(jpg_file, 'rb') as f:  
                    f.seek(-2, 2)
                    buf = f.read()
                    f.close()
                    return buf.endswith(b'\xff\xd9')          
            else:
                return false
                
        except:
            pass

    def is_valid_jpg1(self,jpg_file):
        try:
            bValid = True
            if jpg_file.split('.')[-1].lower() == 'jpg':  
                with open(jpg_file, 'rb') as f:
                    buf=f.read()
                    if not buf.startswith(b'\xff\xd8'):
                        bValid = False
                    elif buf[6:10] in (b'JFIF', b'Exif'):
                        if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                            bValid = False
                    else:
                        try:
                            Image.open(f).verify()
                        except:
                            bValid = False               
            else:  
                return bValid
        except:
            pass
        return bValid
    

    def IsValidImage(self,pathfile):
        bValid = True
        try:
          Image.open(pathfile).verify()
        except:
          bValid = False
        return bValid
    def time(self):
        self.TCP.video_Flag=False
        if  self.is_valid_jpg1('video.jpg') and self.IsValidImage('video.jpg') and self.is_valid_jpg('video.jpg'):
            self.label_Video.setPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8('video.jpg')))
        self.TCP.video_Flag=True
            
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow=mywindow()
    myshow.show();   
    sys.exit(app.exec_())
    


