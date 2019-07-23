#!/usr/bin/python 
# -*- coding: utf-8 -*-
import io
import socket
import struct
import time
import picamera
import gzip
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
from Infrared_Obstacle_Avoidance import *
from threading import Timer
from threading import Thread
from Command import COMMAND as cmd


class video:   
    def __init__(self):
        self.PWM=Motor()
        self.servo=Servo()
        self.led=Led()
        self.ultrasonic=Ultrasonic()
        self.buzzer=Buzzer()
        self.adc=Adc()
        self.light=Light()
        self.infrared=Infrared_Obstacle_Avoidance()
        self.Mode = 'one'
        self.sonic=False
        self.Light=False
        self.Power=False
    
    def get_interface_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                "wlan0"[:15]))[20:24])
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
        except Exception ,  e:
            print "No client connection"
        
        
            
    def Reset(self):
        self.StopTcpServer()
        self.StartTcpServer()
        self.SendVideo=Thread(target=self.sendvideo)
        self.ReadData=Thread(target=self.readdata)
        self.SendVideo.start()
        self.ReadData.start()
        
    def SocketAccept(self):
        self.connection1,self.client_address1 = self.server_socket1.accept()  
        self.connection,self.client_address = self.server_socket.accept()      
        self.connection=self.connection.makefile('rb')
    def sendvideo(self):
        try:
            self.connection,self.client_address = self.server_socket.accept()
            self.connection=self.connection.makefile('rb')
        except:
            pass
        try:
            with picamera.PiCamera() as camera:

                camera.resolution = (400,300)      # pi camera resolution

                camera.framerate = 15               # 15 frames/sec

                time.sleep(2)                       # give 2 secs for camera to initilize

                start = time.time()

                stream = io.BytesIO()

                # send jpeg format video stream

                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    try:
                        self.connection.write(struct.pack('<L', stream.tell()))

                        self.connection.flush()

                        stream.seek(0)

                        self.connection.write(stream.read())
                        if time.time() - start > 600:

                            break

                        stream.seek(0)

                        stream.truncate()
                    except:
                        break
            self.connection.write(struct.pack('<L', 0))
        except:
            print "send video error"
            
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
        except:
            pass            
            
    def readdata(self):
            self.connection1,self.client_address1 = self.server_socket1.accept()
            while True:
                try:
                    AllData=self.connection1.recv(1024)
                    if AllData==None:
                        pass
                    elif AllData=='':
                        self.Reset()
                        break
                    elif AllData==cmd.CMD_CLOSE : 
                        self.Reset()
                        break
                    else:
                        data=AllData.split("#")
                except:
                    continue
                if data==None:
                    continue
                elif (cmd.CMD_MODE[0] in data) or (cmd.CMD_MODE[1] in data) or (cmd.CMD_MODE[2] in data) or (cmd.CMD_MODE[3] in data):
                    if cmd.CMD_MODE[0] in data:
                        self.stopMode()
                        self.Mode='one'
                    elif cmd.CMD_MODE[1] in data:
                        self.stopMode()
                        self.Mode='two'
                        self.lightRun=Thread(target=self.light.run)
                        self.lightRun.start()
                    elif cmd.CMD_MODE[2] in data:
                        self.stopMode()
                        self.Mode='three'
                        self.ultrasonicRun=threading.Thread(target=self.ultrasonic.run)
                        self.ultrasonicRun.start()
                        
                    elif cmd.CMD_MODE[3] in data:
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
                        self.connection1.send(data[0]+'#'+data[1])
                    except:
                        pass
                elif cmd.CMD_SERVO in data:
                    try:
                        data1=int(data[1])
                        data2=int(data[2])
                        data3=int(data[3])
                        data4=int(data[4])
                        if data1==None or data2==None or data2==None or data3==None:
                            continue
                        self.servo.setServoPwm(data1,data2,data3,data4)
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
                    try:
                        self.LedMoD=data[1]
                        if self.LedMoD== '0':
                            stop_thread(Led_Mode)
                            self.led.ledMode(self.LedMoD)
                            time.sleep(0.1)
                            self.led.ledMode(self.LedMoD)
                        else :
                            Led_Mode=Thread(target=self.led.ledMode,args=(data[1],))
                            Led_Mode.start()
                    except:
                        pass
                elif cmd.CMD_SONIC in data:
                    if data[1]==cmd.CMD_START:
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
                    if data[1]==cmd.CMD_START:
                        self.Light=True
                        self.lightTimer = threading.Timer(0.3,self.sendLight)
                        self.lightTimer.start()
                    else:
                        self.Light=False
                elif cmd.CMD_POWER in data:
                    if data[1]==cmd.CMD_START:
                        self.Power=True
                        self.powerTimer = threading.Timer(0.7,self.sendPower)
                        self.powerTimer.start()
                    else:
                        self.Power=False
            self.StopTcpServer()
                                            

    def sendUltrasonic(self):
        if self.sonic==True:
            ADC_Ultrasonic=self.ultrasonic.get_distance()
            if ADC_Ultrasonic==self.ultrasonic.get_distance():
                try:
                    self.connection1.send(cmd.CMD_SONIC+"#"+str(ADC_Ultrasonic))
                except:
                    self.sonic=False
            self.ultrasonicTimer = threading.Timer(0.13,self.sendUltrasonic)
            self.ultrasonicTimer.start()
        else:
            pass
    def sendLight(self):
        if self.Light==True:
            ADC_Light1=self.adc.recvADC(0)
            ADC_Light2=self.adc.recvADC(1)
            if ADC_Light1==self.adc.recvADC(0) and ADC_Light2==self.adc.recvADC(1):  
                try:       
                    self.connection1.send(cmd.CMD_LIGHT+'#'+str(ADC_Light1)+'#'+str(ADC_Light2))
                except:
                    self.Light=False
            self.lightTimer = threading.Timer(0.11,self.sendLight)
            self.lightTimer.start()
        else:
            pass
    def sendPower(self):
        if self.Power==True:
            ADC_Power=self.adc.recvADC(2)
            if ADC_Power==self.adc.recvADC(2):
                try:
                    self.connection1.send(cmd.CMD_POWER+'#'+str(ADC_Power))
                except:
                    pass
                    self.Power==False
            self.powerTimer = threading.Timer(10,self.sendPower)
            self.powerTimer.start()
        else:
            pass            


if __name__=='__main__':
    ultrasonic=Ultrasonic()
    Light=Light()
    Light_run=Thread(target=Light.run)
    Light_run.start()
    time.sleep(10)
    stop_thread(Light_run)

    




