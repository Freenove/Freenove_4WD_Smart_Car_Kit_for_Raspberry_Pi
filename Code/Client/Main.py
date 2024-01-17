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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ProgBar(QObject):
    sigPB = pyqtSignal(int)

    def send(self, text):
        self.sigPB.emit(text)


class SigStr(QObject):
    sigStr = pyqtSignal(str)

    def send(self, text):
        self.sigStr.emit(text)


class mywindow(QMainWindow, Ui_Client):
    def __init__(self):
        global timer
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.endChar = '\n'
        self.intervalChar = '#'
        file = open('IP.txt', 'r')
        self.IP.setText(str(file.readline()))
        file.close()
        self.h = self.IP.text()
        self.TCP = VideoStreaming()
        self.servo1 = 90
        self.servo2 = 90
        self.label_FineServo2.setText("0")
        self.label_FineServo1.setText("0")
        self.img = QImage()
        self.img.load("*.png")
        self.img.save("*.png")
        self.img.load("*.jpg")
        self.img.save("*.jpg")
        self.setWindowIcon(QIcon('image/logo_Mini.png'))
        self.label_Video.setPixmap(QPixmap('image/Raspberry_4WD_M_Car.png'))
        self.W_flag = 0
        self.m_DragPosition = self.pos()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.Key_W = False
        self.Key_A = False
        self.Key_S = False
        self.Key_D = False
        self.Key_Q = False
        self.Key_E = False
        self.Key_Z = False
        self.Key_X = False
        self.Key_Space = False
        self.Wheel_Flag = 1
        self.Rotate_Flag = 1
        self.setFocusPolicy(Qt.StrongFocus)
        self.progress_Power.setMinimum(0)
        self.progress_Power.setMaximum(100)

        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Servo1.setText('90')
        self.label_Servo2.setText('90')
        self.label_Video.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.label_Servo1.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.label_Servo2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.label_FineServo1.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.label_FineServo2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

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

        self.VSlider_Servo2.setMinimum(80)
        self.VSlider_Servo2.setMaximum(180)
        self.VSlider_Servo2.setSingleStep(1)
        self.VSlider_Servo2.setValue(self.servo2)
        self.VSlider_Servo2.valueChanged.connect(self.Change_Up_Down)

        self.checkBox_Led1.setChecked(False)
        self.checkBox_Led1.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led1))
        self.checkBox_Led2.setChecked(False)
        self.checkBox_Led2.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led2))
        self.checkBox_Led3.setChecked(False)
        self.checkBox_Led3.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led3))
        self.checkBox_Led4.setChecked(False)
        self.checkBox_Led4.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led4))
        self.checkBox_Led5.setChecked(False)
        self.checkBox_Led5.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led5))
        self.checkBox_Led6.setChecked(False)
        self.checkBox_Led6.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led6))
        self.checkBox_Led7.setChecked(False)
        self.checkBox_Led7.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led7))
        self.checkBox_Led8.setChecked(False)
        self.checkBox_Led8.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led8))

        self.checkBox_Led_Mode1.setChecked(False)
        self.checkBox_Led_Mode1.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led_Mode1))
        self.checkBox_Led_Mode2.setChecked(False)
        self.checkBox_Led_Mode2.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led_Mode2))
        self.checkBox_Led_Mode3.setChecked(False)
        self.checkBox_Led_Mode3.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led_Mode3))
        self.checkBox_Led_Mode4.setChecked(False)
        self.checkBox_Led_Mode4.stateChanged.connect(lambda: self.LedChange(self.checkBox_Led_Mode4))

        self.Btn_Mode1.setChecked(True)
        self.Btn_Mode1.toggled.connect(lambda: self.on_btn_Mode(self.Btn_Mode1))
        self.Btn_Mode2.setChecked(False)
        self.Btn_Mode2.toggled.connect(lambda: self.on_btn_Mode(self.Btn_Mode2))
        self.Btn_Mode3.setChecked(False)
        self.Btn_Mode3.toggled.connect(lambda: self.on_btn_Mode(self.Btn_Mode3))
        self.Btn_Mode4.setChecked(False)
        self.Btn_Mode4.toggled.connect(lambda: self.on_btn_Mode(self.Btn_Mode4))

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

        self.Btn_Move_Left.pressed.connect(self.on_btn_Moveleft)
        self.Btn_Move_Left.released.connect(self.on_btn_Stop)

        self.Btn_Move_Right.pressed.connect(self.on_btn_Moveright)
        self.Btn_Move_Right.released.connect(self.on_btn_Stop)

        self.Btn_DiaLeft.pressed.connect(self.on_btn_Dialeft)
        self.Btn_DiaLeft.released.connect(self.on_btn_Stop)

        self.Btn_DiaRight.pressed.connect(self.on_btn_Diaright)
        self.Btn_DiaRight.released.connect(self.on_btn_Stop)

        self.Btn_DiaDLeft.pressed.connect(self.on_btn_Diad_left)
        self.Btn_DiaDLeft.released.connect(self.on_btn_Stop)

        self.Btn_DiaDRight.pressed.connect(self.on_btn_Diad_right)
        self.Btn_DiaDRight.released.connect(self.on_btn_Stop)

        self.Btn_Video.clicked.connect(self.on_btn_video)

        self.Btn_Up.clicked.connect(self.on_btn_Up)
        self.Btn_Left.clicked.connect(self.on_btn_Left)
        self.Btn_Down.clicked.connect(self.on_btn_Down)
        self.Btn_Home.clicked.connect(self.on_btn_Home)
        self.Btn_Right.clicked.connect(self.on_btn_Right)
        self.Btn_Tracking_Faces.clicked.connect(self.Tracking_Face)
        self.Btn_wheel.clicked.connect(self.on_btn_wheelchange)
        self.Btn_Rotate.clicked.connect(self.on_btn_rotate)
        self.Btn_Buzzer.pressed.connect(self.on_btn_Buzzer)
        self.Btn_Buzzer.released.connect(self.on_btn_Buzzer)

        self.Btn_Connect.clicked.connect(self.on_btn_Connect)

        self.Window_Min.clicked.connect(self.windowMinimumed)
        self.Window_Close.clicked.connect(self.close)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)

        self.Pb = ProgBar()
        self.Pb.sigPB.connect(self.onPbChanged)

        self.U = SigStr()
        self.U.sigStr.connect(self.onUsonicChanged)

        self.L = SigStr()
        self.L.sigStr.connect(self.onLightChanged)

    def onPbChanged(self, value):
        self.progress_Power.setValue(value)

    def onUsonicChanged(self, value):
        self.Ultrasonic.setText(value)

    def onLightChanged(self, value):
        self.Light.setText(value)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Up):
            self.on_btn_Up()
        elif (event.key() == Qt.Key_Left):
            self.on_btn_Left()
        elif (event.key() == Qt.Key_Down):
            self.on_btn_Down()
        elif (event.key() == Qt.Key_Right):
            self.on_btn_Right()
        elif (event.key() == Qt.Key_Home):
            self.on_btn_Home()

        if (event.key() == Qt.Key_R):
            if self.Btn_Mode1.isChecked() is True:
                self.Btn_Mode2.setChecked(True)
            elif self.Btn_Mode2.isChecked() is True:
                self.Btn_Mode3.setChecked(True)
            elif self.Btn_Mode3.isChecked() is True:
                self.Btn_Mode4.setChecked(True)
            elif self.Btn_Mode4.isChecked() is True:
                self.Btn_Mode1.setChecked(True)

        if (event.key() == Qt.Key_L):
            count = 0
            if self.checkBox_Led_Mode1.isChecked() is True:
                self.checkBox_Led_Mode2.setChecked(True)
            elif self.checkBox_Led_Mode2.isChecked() is True:
                self.checkBox_Led_Mode3.setChecked(True)
            elif self.checkBox_Led_Mode3.isChecked() is True:
                self.checkBox_Led_Mode4.setChecked(True)
            elif self.checkBox_Led_Mode4.isChecked() is True:
                self.checkBox_Led_Mode1.setChecked(True)

            for i in range(1, 5):
                checkBox_Led_Mode = getattr(self, "checkBox_Led_Mode%d" % i)
                if checkBox_Led_Mode.isChecked() is False:
                    count += 1
                else:
                    break
            if count == 4:
                self.checkBox_Led_Mode1.setChecked(True)

        if (event.key() == Qt.Key_C):
            self.on_btn_Connect()
        if (event.key() == Qt.Key_V):
            self.on_btn_video()
        if (event.key() == Qt.Key_O):
            self.on_btn_rotate()

        if (event.key() == Qt.Key_1):
            if self.checkBox_Led1.isChecked() is True:
                self.checkBox_Led1.setChecked(False)
            else:
                self.checkBox_Led1.setChecked(True)
        elif (event.key() == Qt.Key_2):
            if self.checkBox_Led2.isChecked() is True:
                self.checkBox_Led2.setChecked(False)
            else:
                self.checkBox_Led2.setChecked(True)
        elif (event.key() == Qt.Key_3):
            if self.checkBox_Led3.isChecked() is True:
                self.checkBox_Led3.setChecked(False)
            else:
                self.checkBox_Led3.setChecked(True)
        elif (event.key() == Qt.Key_4):
            if self.checkBox_Led4.isChecked() is True:
                self.checkBox_Led4.setChecked(False)
            else:
                self.checkBox_Led4.setChecked(True)
        elif (event.key() == Qt.Key_5):
            if self.checkBox_Led5.isChecked() is True:
                self.checkBox_Led5.setChecked(False)
            else:
                self.checkBox_Led5.setChecked(True)
        elif (event.key() == Qt.Key_6):
            if self.checkBox_Led6.isChecked() is True:
                self.checkBox_Led6.setChecked(False)
            else:
                self.checkBox_Led6.setChecked(True)
        elif (event.key() == Qt.Key_7):
            if self.checkBox_Led7.isChecked() is True:
                self.checkBox_Led7.setChecked(False)
            else:
                self.checkBox_Led7.setChecked(True)
        elif (event.key() == Qt.Key_8):
            if self.checkBox_Led8.isChecked() is True:
                self.checkBox_Led8.setChecked(False)
            else:
                self.checkBox_Led8.setChecked(True)

        if event.isAutoRepeat():
            pass
        else:
            if event.key() == Qt.Key_W:
                self.on_btn_ForWard()
                self.Key_W = True
            elif event.key() == Qt.Key_S:
                self.on_btn_BackWard()
                self.Key_S = True
            elif event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_A:
                self.on_btn_Turn_Left()
                self.Key_A = True
            elif event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_D:
                self.on_btn_Turn_Right()
                self.Key_D = True
            elif event.key() == Qt.Key_A:
                self.on_btn_Moveleft()
                self.Key_A = True
            elif event.key() == Qt.Key_D:
                self.on_btn_Moveright()
                self.Key_D = True

            elif event.key() == Qt.Key_Q:
                self.on_btn_Dialeft()
                self.Key_Q = True
            elif event.key() == Qt.Key_E:
                self.on_btn_Diaright()
                self.Key_E = True
            elif event.key() == Qt.Key_Z:
                self.on_btn_Diad_left()
                self.Key_Z = True
            elif event.key() == Qt.Key_X:
                self.on_btn_Diad_right()
                self.Key_X = True
            elif event.key() == Qt.Key_Space:
                self.on_btn_Buzzer()
                self.Key_Space = True

    def keyReleaseEvent(self, event):

        if (event.key() == Qt.Key_W):
            time.sleep(0.05)
            if (event.key() == Qt.Key_W):
                if not (event.isAutoRepeat()) and self.Key_W is True:
                    self.on_btn_Stop()
                    self.Key_W = False
        elif (event.key() == Qt.Key_A):
            if not (event.isAutoRepeat()) and self.Key_A is True:
                self.on_btn_Stop()
                self.Key_A = False
        elif (event.key() == Qt.Key_S):
            if not (event.isAutoRepeat()) and self.Key_S is True:
                self.on_btn_Stop()
                self.Key_S = False
        elif (event.key() == Qt.Key_D):
            if not (event.isAutoRepeat()) and self.Key_D is True:
                self.on_btn_Stop()
                self.Key_D = False
        elif (event.key() == Qt.Key_Q):
            if not (event.isAutoRepeat()) and self.Key_Q is True:
                self.on_btn_Stop()
                self.Key_Q = False
        elif (event.key() == Qt.Key_E):
            if not (event.isAutoRepeat()) and self.Key_E is True:
                self.on_btn_Stop()
                self.Key_E = False
        elif (event.key() == Qt.Key_Z):
            if not (event.isAutoRepeat()) and self.Key_Z is True:
                self.on_btn_Stop()
                self.Key_Z = False
        elif (event.key() == Qt.Key_X):
            if not (event.isAutoRepeat()) and self.Key_X is True:
                self.on_btn_Stop()
                self.Key_X = False

        if (event.key() == Qt.Key_Space):
            if not (event.isAutoRepeat()) and self.Key_Space is True:
                self.on_btn_Buzzer()
                self.Key_Space = False

    def on_btn_ForWard(self):
        if self.Wheel_Flag:
            if self.Rotate_Flag:
                M_ForWard = self.intervalChar + str(0) + self.intervalChar + str(1500) + self.intervalChar + str(
                    0) + self.intervalChar + str(0) + self.endChar
                self.TCP.sendData(cmd.CMD_M_MOTOR + M_ForWard)
            else:
                R_ForWard = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                    0) + self.intervalChar + str(1500) + self.endChar
                self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_ForWard)
        else:
            ForWard = self.intervalChar + str(1500) + self.intervalChar + str(1500) + self.intervalChar + str(
                1500) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_MOTOR + ForWard)

    def on_btn_Turn_Left(self):
        if self.Wheel_Flag:
            M_Turn_Left = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                90) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + M_Turn_Left)
        else:
            Turn_Left = self.intervalChar + str(-1500) + self.intervalChar + str(-1500) + self.intervalChar + str(
                1500) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_MOTOR + Turn_Left)

    def on_btn_BackWard(self):
        if self.Wheel_Flag:
            if self.Rotate_Flag:
                M_BackWard = self.intervalChar + str(180) + self.intervalChar + str(1500) + self.intervalChar + str(
                    0) + self.intervalChar + str(0) + self.endChar
                self.TCP.sendData(cmd.CMD_M_MOTOR + M_BackWard)
            else:
                R_BackWard = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                    180) + self.intervalChar + str(1500) + self.endChar
                self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_BackWard)
        else:
            BackWard = self.intervalChar + str(-1500) + self.intervalChar + str(-1500) + self.intervalChar + str(
                -1500) + self.intervalChar + str(-1500) + self.endChar
            self.TCP.sendData(cmd.CMD_MOTOR + BackWard)

    def on_btn_Turn_Right(self):
        if self.Wheel_Flag:
            M_Turn_Right = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                -90) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + M_Turn_Right)
        else:
            Turn_Right = self.intervalChar + str(-1500) + self.intervalChar + str(-1500) + self.intervalChar + str(
                1500) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_MOTOR + Turn_Right)

    def on_btn_Stop(self):
        if self.Wheel_Flag:
            if self.Rotate_Flag:
                M_Stop = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                    0) + self.intervalChar + str(0) + self.endChar
                self.TCP.sendData(cmd.CMD_M_MOTOR + M_Stop)
            else:
                R_Stop = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                    0) + self.intervalChar + str(0) + self.endChar
                self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_Stop)
        else:
            Stop = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                0) + self.intervalChar + str(0) + self.endChar
            self.TCP.sendData(cmd.CMD_MOTOR + Stop)

    def on_btn_Moveleft(self):
        if self.Rotate_Flag:
            M_Move_Left = self.intervalChar + str(90) + self.intervalChar + str(1500) + self.intervalChar + str(
                0) + self.intervalChar + str(0) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + M_Move_Left)
        else:
            R_Move_Left = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                90) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_Move_Left)

    def on_btn_Moveright(self):
        if self.Rotate_Flag:
            M_Move_Right = self.intervalChar + str(-90) + self.intervalChar + str(1500) + self.intervalChar + str(
                0) + self.intervalChar + str(0) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + M_Move_Right)
        else:
            R_Move_Right = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                -90) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_Move_Right)

    def on_btn_Dialeft(self):
        if self.Rotate_Flag:
            Dialeft = self.intervalChar + str(45) + self.intervalChar + str(1500) + self.intervalChar + str(
                0) + self.intervalChar + str(0) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + Dialeft)
        else:
            R_Dialeft = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                135) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_Dialeft)

    def on_btn_Diaright(self):
        if self.Rotate_Flag:
            Diaright = self.intervalChar + str(-45) + self.intervalChar + str(1500) + self.intervalChar + str(
                0) + self.intervalChar + str(0) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + Diaright)
        else:
            R_Diaright = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                135) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_Diaright)

    def on_btn_Diad_left(self):
        if self.Rotate_Flag:
            Diadleft = self.intervalChar + str(135) + self.intervalChar + str(1500) + self.intervalChar + str(
                0) + self.intervalChar + str(0) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + Diadleft)
        else:
            R_Diadleft = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                135) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_Diadleft)

    def on_btn_Diad_right(self):
        if self.Rotate_Flag:
            Diadright = self.intervalChar + str(-135) + self.intervalChar + str(1500) + self.intervalChar + str(
                0) + self.intervalChar + str(0) + self.endChar
            self.TCP.sendData(cmd.CMD_M_MOTOR + Diadright)
        else:
            R_Diadright = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(
                -135) + self.intervalChar + str(1500) + self.endChar
            self.TCP.sendData(cmd.CMD_CAR_ROTATE + R_Diadright)

    def on_btn_wheelchange(self):
        if self.Wheel_Flag:
            self.Btn_Move_Left.hide()
            self.Btn_Move_Right.hide()
            self.Btn_DiaLeft.hide()
            self.Btn_DiaRight.hide()
            self.Btn_DiaDLeft.hide()
            self.Btn_DiaDRight.hide()
            self.Btn_Rotate.hide()
            self.Btn_Turn_Left.move(80, 520)
            self.Btn_Turn_Right.move(300, 520)
            self.Btn_wheel.setText("Ordinaly_wheels")
            self.label_Video.setPixmap(QPixmap('image/Raspberry_4WD_Car.png'))
            self.Wheel_Flag = 0
        else:
            self.Btn_Move_Left.show()
            self.Btn_Move_Right.show()
            self.Btn_DiaLeft.show()
            self.Btn_DiaRight.show()
            self.Btn_DiaDLeft.show()
            self.Btn_DiaDRight.show()
            self.Btn_Rotate.show()
            self.Btn_Turn_Left.move(0, 520)
            self.Btn_Turn_Right.move(380, 520)
            self.Btn_wheel.setText("Mecanum_wheels")
            self.label_Video.setPixmap(QPixmap('image/Raspberry_4WD_M_Car.png'))
            self.Wheel_Flag = 1

    def on_btn_rotate(self):
        if self.Rotate_Flag:
            self.Btn_Rotate.setText("Rotate-Off")
            self.Rotate_Flag = 0
        else:
            self.Btn_Rotate.setText("Rotate-On")
            self.Rotate_Flag = 1

    def on_btn_video(self):
        if self.Btn_Video.text() == 'Open Video':
            self.timer.start(34)
            self.Btn_Video.setText('Close Video')
        elif self.Btn_Video.text() == 'Close Video':
            self.timer.stop()
            self.Btn_Video.setText('Open Video')

    def on_btn_Up(self):
        self.servo2 = self.servo2 + 10
        if self.servo2 >= 180:
            self.servo2 = 180
        self.VSlider_Servo2.setValue(self.servo2)

    def on_btn_Left(self):
        self.servo1 = self.servo1 - 10
        if self.servo1 <= 0:
            self.servo1 = 0
        self.HSlider_Servo1.setValue(self.servo1)

    def on_btn_Down(self):
        self.servo2 = self.servo2 - 10
        if self.servo2 <= 80:
            self.servo2 = 80
        self.VSlider_Servo2.setValue(self.servo2)

    def on_btn_Right(self):
        self.servo1 = self.servo1 + 10
        if self.servo1 >= 180:
            self.servo1 = 180
        self.HSlider_Servo1.setValue(self.servo1)

    def on_btn_Home(self):
        self.servo1 = 90
        self.servo2 = 90
        self.HSlider_Servo1.setValue(self.servo1)
        self.VSlider_Servo2.setValue(self.servo2)

    def on_btn_Buzzer(self):
        if self.Btn_Buzzer.text() == 'Buzzer':
            self.TCP.sendData(cmd.CMD_BUZZER + self.intervalChar + '1' + self.endChar)
            self.Btn_Buzzer.setText('Noise')
        else:
            self.TCP.sendData(cmd.CMD_BUZZER + self.intervalChar + '0' + self.endChar)
            self.Btn_Buzzer.setText('Buzzer')

    def on_btn_Ultrasonic(self):
        if self.Ultrasonic.text() == "Ultrasonic":
            self.TCP.sendData(cmd.CMD_SONIC + self.intervalChar + '1' + self.endChar)
        else:
            self.TCP.sendData(cmd.CMD_SONIC + self.intervalChar + '0' + self.endChar)
            self.Ultrasonic.setText("Ultrasonic")

    def on_btn_Light(self):
        if self.Light.text() == "Light":
            self.TCP.sendData(cmd.CMD_LIGHT + self.intervalChar + '1' + self.endChar)
        else:
            self.TCP.sendData(cmd.CMD_LIGHT + self.intervalChar + '0' + self.endChar)
            self.Light.setText("Light")

    def Change_Left_Right(self):  # Left or Right
        self.servo1 = self.HSlider_Servo1.value()
        self.TCP.sendData(cmd.CMD_SERVO + self.intervalChar + '0' + self.intervalChar + str(self.servo1) + self.endChar)
        self.label_Servo1.setText("%d" % self.servo1)

    def Change_Up_Down(self):  # Up or Down
        self.servo2 = self.VSlider_Servo2.value()
        self.TCP.sendData(cmd.CMD_SERVO + self.intervalChar + '1' + self.intervalChar + str(self.servo2) + self.endChar)
        self.label_Servo2.setText("%d" % self.servo2)

    def Fine_Tune_Left_Right(self):  # fine tune Left or Right
        self.label_FineServo1.setText(str(self.HSlider_FineServo1.value()))
        data = self.servo1 + self.HSlider_FineServo1.value()
        self.TCP.sendData(cmd.CMD_SERVO + self.intervalChar + '0' + self.intervalChar + str(data) + self.endChar)

    def Fine_Tune_Up_Down(self):  # fine tune Up or Down
        self.label_FineServo2.setText(str(self.HSlider_FineServo2.value()))
        data = self.servo2 + self.HSlider_FineServo2.value()
        self.TCP.sendData(cmd.CMD_SERVO + self.intervalChar + '1' + self.intervalChar + str(data) + self.endChar)

    def windowMinimumed(self):
        self.showMinimized()

    def LedChange(self, b):
        R = self.Color_R.text()
        G = self.Color_G.text()
        B = self.Color_B.text()
        led_Off = self.intervalChar + str(0) + self.intervalChar + str(0) + self.intervalChar + str(0) + self.endChar
        color = self.intervalChar + str(R) + self.intervalChar + str(G) + self.intervalChar + str(B) + self.endChar
        if b.text() == "Led1":
            self.led_Index = str(0x01)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led2":
            self.led_Index = str(0x02)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led3":
            self.led_Index = str(0x04)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led4":
            self.led_Index = str(0x08)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led5":
            self.led_Index = str(0x10)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led6":
            self.led_Index = str(0x20)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led7":
            self.led_Index = str(0x40)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led8":
            self.led_Index = str(0x80)
            if b.isChecked() is True:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + color)
            else:
                self.TCP.sendData(cmd.CMD_LED + self.intervalChar + self.led_Index + led_Off)
        if b.text() == "Led_Mode1":
            if b.isChecked() is True:
                self.checkBox_Led_Mode2.setChecked(False)
                self.checkBox_Led_Mode3.setChecked(False)
                self.checkBox_Led_Mode4.setChecked(False)
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '1' + self.endChar)
            else:
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '0' + self.endChar)
        if b.text() == "Led_Mode2":
            if b.isChecked() is True:

                self.checkBox_Led_Mode1.setChecked(False)
                self.checkBox_Led_Mode3.setChecked(False)
                self.checkBox_Led_Mode4.setChecked(False)
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '2' + self.endChar)
            else:
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '0' + self.endChar)
        if b.text() == "Led_Mode3":
            if b.isChecked() is True:
                self.checkBox_Led_Mode2.setChecked(False)
                self.checkBox_Led_Mode1.setChecked(False)
                self.checkBox_Led_Mode4.setChecked(False)
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '3' + self.endChar)
            else:
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '0' + self.endChar)
        if b.text() == "Led_Mode4":
            if b.isChecked() is True:
                self.checkBox_Led_Mode2.setChecked(False)
                self.checkBox_Led_Mode3.setChecked(False)
                self.checkBox_Led_Mode1.setChecked(False)
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '4' + self.endChar)
            else:
                self.TCP.sendData(cmd.CMD_LED_MOD + self.intervalChar + '0' + self.endChar)

    def on_btn_Mode(self, Mode):
        if Mode.text() == "M-Free":
            if Mode.isChecked() is True:
                # self.timer.start(34)
                self.TCP.sendData(cmd.CMD_MODE + self.intervalChar + 'one' + self.endChar)
        if Mode.text() == "M-Light":
            if Mode.isChecked() is True:
                # self.timer.stop()
                self.TCP.sendData(cmd.CMD_MODE + self.intervalChar + 'two' + self.endChar)
        if Mode.text() == "M-Sonic":
            if Mode.isChecked() is True:
                # self.timer.stop()
                self.TCP.sendData(cmd.CMD_MODE + self.intervalChar + 'three' + self.endChar)
        if Mode.text() == "M-Line":
            if Mode.isChecked() is True:
                # self.timer.stop()
                self.TCP.sendData(cmd.CMD_MODE + self.intervalChar + 'four' + self.endChar)

    def on_btn_Connect(self):
        if self.Btn_Connect.text() == "Connect":
            self.h = self.IP.text()
            self.TCP.StartTcpClient(self.h, )
            file = open('IP.txt', 'w')
            file.write(self.IP.text())
            file.close()
            try:
                self.streaming = Thread(target=self.TCP.streaming, args=(self.h,))
                self.streaming.start()
            except:
                print('video error')
            try:
                self.recv = Thread(target=self.recvmassage)
                self.recv.start()
            except:
                print('recv error')
            self.Btn_Connect.setText("Disconnect")
            print('Server address:' + str(self.h) + '\n')
        elif self.Btn_Connect.text() == "Disconnect":
            self.Btn_Connect.setText("Connect")
            try:
                stop_thread(self.recv)
                stop_thread(self.power)
                stop_thread(self.streaming)
            except:
                pass
            self.TCP.StopTcpcClient()

    def close(self):
        self.timer.stop()
        try:
            stop_thread(self.recv)
            stop_thread(self.streaming)
        except:
            pass
        self.TCP.StopTcpcClient()
        try:
            os.remove("video.jpg")
        except:
            pass
        QCoreApplication.instance().quit()
        sys.exit(0)

    def Power(self):
        while True:
            try:
                self.TCP.sendData(cmd.CMD_POWER + self.endChar)
                time.sleep(60)
            except:
                break

    def recvmassage(self):
        self.TCP.socket1_connect(self.h)
        self.power = Thread(target=self.Power)
        self.power.start()
        restCmd = ""

        while True:
            Alldata = restCmd + str(self.TCP.recvData())
            restCmd = ""
            print(Alldata)
            if Alldata == "":
                break
            else:
                cmdArray = Alldata.split("\n")
                if (cmdArray[-1] != ""):
                    restCmd = cmdArray[-1]
                    cmdArray = cmdArray[:-1]
            for oneCmd in cmdArray:
                Massage = oneCmd.split("#")
                if cmd.CMD_SONIC in Massage:
                    # self.Ultrasonic.setText('Obstruction:%s cm' % Massage[1])
                    u = 'Obstruction:%s cm' % Massage[1]
                    self.U.send(u)
                elif cmd.CMD_LIGHT in Massage:
                    # self.Light.setText("Left:" + Massage[1] + 'V' + ' ' + "Right:" + Massage[2] + 'V')
                    l = "Left:" + Massage[1] + 'V' + ' ' + "Right:" + Massage[2] + 'V'
                    self.L.send(l)
                elif cmd.CMD_POWER in Massage:
                    percent_power = int((float(Massage[1]) - 7) / 1.40 * 100)
                    # self.progress_Power.setValue(percent_power)
                    self.Pb.send(percent_power)

    def is_valid_jpg(self, jpg_file):
        try:
            bValid = True
            if jpg_file.split('.')[-1].lower() == 'jpg':
                with open(jpg_file, 'rb') as f:
                    buf = f.read()
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

    def Tracking_Face(self):
        if self.Btn_Tracking_Faces.text() == "Tracing-On":
            self.Btn_Tracking_Faces.setText("Tracing-Off")
        else:
            self.Btn_Tracking_Faces.setText("Tracing-On")
    def find_Face(self,face_x,face_y):
        if face_x!=0 and face_y!=0:
            offset_x=float(face_x/400-0.5)*2
            offset_y=float(face_y/300-0.5)*2
            delta_degree_x = int(4* offset_x)
            delta_degree_y = int(-4 * offset_y)
            self.servo1=self.servo1+delta_degree_x
            self.servo2=self.servo2+delta_degree_y
            if offset_x > -0.15 and offset_y >-0.15 and offset_x < 0.15 and offset_y <0.15:
                pass
            else:
                self.HSlider_Servo1.setValue(self.servo1)
                self.VSlider_Servo2.setValue(self.servo2)

    def time(self):
        self.TCP.video_Flag = False
        try:
            if self.is_valid_jpg('video.jpg'):
                self.label_Video.setPixmap(QPixmap('video.jpg'))
                if self.Btn_Tracking_Faces.text() == "Tracing-Off":
                    self.find_Face(self.TCP.face_x, self.TCP.face_y)
        except Exception as e:
            print(e)
        self.TCP.video_Flag = True


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
