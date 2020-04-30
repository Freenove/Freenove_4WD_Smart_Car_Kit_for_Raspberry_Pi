#!/usr/bin/python 
# -*- coding: utf-8 -*-
import io
import socket
import struct
import time
import picamera
import fcntl
import  sys
import threading
from Motor import *
from servo import *
from Led import *
from Buzzer import *
from ADC import *
from Thread import *
from Light import *
from Ultrasonic import *
from Line_Tracking import *
from threading import Timer
from threading import Thread
from Command import COMMAND as cmd

class Server:   
    def __init__(self):
        self.PWM=Motor()
        self.servo=Servo()
        self.led=Led()
        self.ultrasonic=Ultrasonic()
        self.buzzer=Buzzer()
        self.adc=Adc()
        self.light=Light()
        self.infrared=Line_Tracking()
        self.tcp_Flag = True
        self.sonic=False
        self.Light=False
        self.Mode = 'one'
        self.endChar='\n'
        self.intervalChar='#'
    def get_interface_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                            0x8915,
                                            struct.pack('256s',b'wlan0'[:15])
                                            )[20:24])
    def StartTcpServer(self):
        HOST=str(self.get_interface_ip())
        self.server_socket1 = socket.socket()
        self.server_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket1.bind((HOST, 5000))
        self.server_socket1.listen(1)
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket.bind((HOST, 8000))              
        self.server_socket.listen(1)
        print('Server address: '+HOST)
        
        
    def StopTcpServer(self):
        try:
            self.connection.close()
            self.connection1.close()
        except Exception as e:
            print ('\n'+"No client connection")
         
    def Reset(self):
        self.StopTcpServer()
        self.StartTcpServer()
        self.SendVideo=Thread(target=self.sendvideo)
        self.ReadData=Thread(target=self.readdata)
        self.SendVideo.start()
        self.ReadData.start()
    def send(self,data):
        self.connection1.send(data.encode('utf-8'))    
    def sendvideo(self):
        try:
            self.connection,self.client_address = self.server_socket.accept()
            self.connection=self.connection.makefile('wb')
        except:
            pass
        self.server_socket.close()
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (400,300)      # pi camera resolution
                camera.framerate = 15               # 15 frames/sec
                time.sleep(2)                       # give 2 secs for camera to initilize
                start = time.time()
                stream = io.BytesIO()
                # send jpeg format video stream
                print ("Start transmit ... ")
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    try:
                        self.connection.flush()
                        stream.seek(0)
                        b = stream.read()
                        length=len(b)
                        if length >5120000:
                            continue
                        lengthBin = struct.pack('L', length)
                        self.connection.write(lengthBin)
                        self.connection.write(b)
                        stream.seek(0)
                        stream.truncate()
                    except Exception as e:
                        print(e)
                        print ("End transmit ... " )
                        break
        except:
            #print "Camera unintall"
            pass
                 
    def stopMode(self):
        try:
            stop_thread(self.infraredRun)
            self.PWM.setMotorModel(0,0,0,0)
        except:
            pass
        try:
            stop_thread(self.lightRun)
            self.PWM.setMotorModel(0,0,0,0)
        except:
            pass            
        try:
            stop_thread(self.ultrasonicRun)
            self.PWM.setMotorModel(0,0,0,0)
            self.servo.setServoPwm('0',90)
            self.servo.setServoPwm('1',90)
        except:
            pass
        
    def readdata(self):
        try:
            try:
                self.connection1,self.client_address1 = self.server_socket1.accept()
                print ("Client connection successful !")
            except:
                print ("Client connect failed")
            restCmd=""
            self.server_socket1.close()
            while True:
                try:
                    AllData=restCmd+self.connection1.recv(1024).decode('utf-8')
                except:
                    if self.tcp_Flag:
                        self.Reset()
                    break
                print(AllData)
                if len(AllData) < 5:
                    restCmd=AllData
                    if restCmd=='' and self.tcp_Flag:
                        self.Reset()
                        break
                restCmd=""
                if AllData=='':
                    break
                else:
                    cmdArray=AllData.split("\n")
                    if(cmdArray[-1] != ""):
                        restCmd=cmdArray[-1]
                        cmdArray=cmdArray[:-1]     
            
                for oneCmd in cmdArray:
                    data=oneCmd.split("#")
                    if data==None:
                        continue
                    elif cmd.CMD_MODE in data:
                        if data[1]=='one':
                            self.stopMode()
                            self.Mode='one'
                        elif data[1]=='two':
                            self.stopMode()
                            self.Mode='two'
                            self.lightRun=Thread(target=self.light.run)
                            self.lightRun.start()
                        elif data[1]=='three':
                            self.stopMode()
                            self.Mode='three'
                            self.ultrasonicRun=threading.Thread(target=self.ultrasonic.run)
                            self.ultrasonicRun.start()
                        elif data[1]=='four':
                            self.stopMode()
                            self.Mode='four'
                            self.infraredRun=threading.Thread(target=self.infrared.run)
                            self.infraredRun.start()
                            
                    elif (cmd.CMD_MOTOR in data) and self.Mode=='one':
                        try:
                            data1=int(data[1])
                            data2=int(data[2])
                            data3=int(data[3])
                            data4=int(data[4])
                            if data1==None or data2==None or data2==None or data3==None:
                                continue
                            self.PWM.setMotorModel(data1,data2,data3,data4)
                        except:
                            pass
                    elif cmd.CMD_SERVO in data:
                        try:
                            data1=data[1]
                            data2=int(data[2])
                            if data1==None or data2==None:
                                continue
                            self.servo.setServoPwm(data1,data2)
                        except:
                            pass

                    elif cmd.CMD_LED in data:
                        try:
                            data1=int(data[1])
                            data2=int(data[2])
                            data3=int(data[3])
                            data4=int(data[4])
                            if data1==None or data2==None or data2==None or data3==None:
                                continue
                            self.led.ledIndex(data1,data2,data3,data4)
                        except:
                            pass
                    elif cmd.CMD_LED_MOD in data:
                        self.LedMoD=data[1]
                        if self.LedMoD== '0':
                            try:
                                stop_thread(Led_Mode)
                            except:
                                pass
                            self.led.ledMode(self.LedMoD)
                            time.sleep(0.1)
                            self.led.ledMode(self.LedMoD)
                        else :
                            try:
                                stop_thread(Led_Mode)
                            except:
                                pass
                            time.sleep(0.1)
                            Led_Mode=Thread(target=self.led.ledMode,args=(data[1],))
                            Led_Mode.start()
                    elif cmd.CMD_SONIC in data:
                        if data[1]=='1':
                            self.sonic=True
                            self.ultrasonicTimer = threading.Timer(0.5,self.sendUltrasonic)
                            self.ultrasonicTimer.start()
                        else:
                            self.sonic=False
                    elif cmd.CMD_BUZZER in data:
                        try:
                            self.buzzer.run(data[1])
                        except:
                            pass
                    elif cmd.CMD_LIGHT in data:
                        if data[1]=='1':
                            self.Light=True
                            self.lightTimer = threading.Timer(0.3,self.sendLight)
                            self.lightTimer.start()
                        else:
                            self.Light=False
                    elif cmd.CMD_POWER in data:
                        ADC_Power=self.adc.recvADC(2)*3
                        try:
                            self.send(cmd.CMD_POWER+'#'+str(ADC_Power)+'\n')
                        except:
                            pass
        except Exception as e: 
            print(e)
        self.StopTcpServer()    
    def sendUltrasonic(self):
        if self.sonic==True:
            ADC_Ultrasonic=self.ultrasonic.get_distance()
            if ADC_Ultrasonic==self.ultrasonic.get_distance():
                try:
                    self.send(cmd.CMD_SONIC+"#"+str(ADC_Ultrasonic)+'\n')
                except:
                    self.sonic=False
            self.ultrasonicTimer = threading.Timer(0.13,self.sendUltrasonic)
            self.ultrasonicTimer.start()
    def sendLight(self):
        if self.Light==True:
            ADC_Light1=self.adc.recvADC(0)
            ADC_Light2=self.adc.recvADC(1) 
            try:
                self.send(cmd.CMD_LIGHT+'#'+str(ADC_Light1)+'#'+str(ADC_Light2)+'\n')
            except:
                self.Light=False
            self.lightTimer = threading.Timer(0.17,self.sendLight)
            self.lightTimer.start()
    def Power(self):
        while True:
            ADC_Power=self.adc.recvADC(2)*3
            time.sleep(3)
            if ADC_Power < 6.8:
                for i in range(4):
                    self.buzzer.run('1')
                    time.sleep(0.1)
                    self.buzzer.run('0')
                    time.sleep(0.1)
            elif ADC_Power< 7:
                for i in range(2):
                    self.buzzer.run('1')
                    time.sleep(0.1)
                    self.buzzer.run('0')
                    time.sleep(0.1)
            else:
                self.buzzer.run('0')
if __name__=='__main__':
    pass
