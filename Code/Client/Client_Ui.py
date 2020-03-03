# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Freenove\Desktop\树莓派四轮车项目\四轮车（python3+pyqt5）\Client_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Client(object):
    def setupUi(self, Client):
        Client.setObjectName("Client")
        Client.resize(760, 610)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Client.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        Client.setFont(font)
        Client.setStyleSheet("QWidget{\n"
"background:#484848;\n"
"}\n"
"QAbstractButton{\n"
"border-style:none;\n"
"border-radius:0px;\n"
"padding:5px;\n"
"color:#DCDCDC;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #484848,stop:1 #383838);\n"
"}\n"
"QAbstractButton:hover{\n"
"color:#FFFFFF;\n"
"background-color:#00BB9E;\n"
"}\n"
"QAbstractButton:pressed{\n"
"color:#DCDCDC;\n"
"border-style:solid;\n"
"border-width:0px 0px 0px 2px;\n"
"padding:4px 4px 4px 2px;\n"
"border-color:#00BB9E;\n"
"background-color:#444444;\n"
"}\n"
"QLabel{\n"
"color:#DCDCDC;\n"
"border:1px solid #242424;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #484848,stop:1 #383838);\n"
"}\n"
"QLabel:focus{\n"
"border:1px solid #00BB9E;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #646464,stop:1 #525252);\n"
"}\n"
"QLineEdit{\n"
"border:1px solid #242424;\n"
"border-radius:3px;\n"
"padding:2px;\n"
"background:none;\n"
"selection-background-color:#484848;\n"
"selection-color:#DCDCDC;\n"
"}\n"
"QLineEdit:focus,QLineEdit:hover{\n"
"border:1px solid #242424;\n"
"}\n"
"QLineEdit{\n"
"border:1px solid #242424;\n"
"border-radius:3px;\n"
"padding:2px;\n"
"background:none;\n"
"selection-background-color:#484848;\n"
"selection-color:#DCDCDC;\n"
"}\n"
"\n"
"QLineEdit:focus,QLineEdit:hover{\n"
"border:1px solid #242424;\n"
"}\n"
"QLineEdit{\n"
"lineedit-password-character:9679;\n"
"}\n"
"QSlider::groove:horizontal,QSlider::add-page:horizontal{\n"
"height:3px;\n"
"border-radius:3px;\n"
"background:#18181a;\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal{\n"
"height:8px;\n"
"border-radius:3px;\n"
"background:#008aff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal{\n"
"width:12px;\n"
"margin-top:-5px;\n"
"margin-bottom:-4px;\n"
"border-radius:6px;\n"
"background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #565656,stop:0.8 #565656);\n"
"}\n"
"\n"
"\n"
"QSlider::groove:vertical,QSlider::sub-page:vertical{\n"
"width:3px;\n"
"border-radius:3px;\n"
"background:#18181a;\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:vertical{\n"
"width:8px;\n"
"border-radius:3px;\n"
"background:#008aff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:vertical{\n"
"height:12px;\n"
"margin-left:-5px;\n"
"margin-right:-4px;\n"
"border-radius:6px;\n"
"background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #565656,stop:0.8 #565656);\n"
"}\n"
"")
        self.Btn_ForWard = QtWidgets.QPushButton(Client)
        self.Btn_ForWard.setGeometry(QtCore.QRect(120, 460, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_ForWard.setFont(font)
        self.Btn_ForWard.setStyleSheet("")
        self.Btn_ForWard.setObjectName("Btn_ForWard")
        self.name = QtWidgets.QLabel(Client)
        self.name.setGeometry(QtCore.QRect(0, 1, 660, 40))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(28)
        font.setBold(False)
        font.setWeight(50)
        self.name.setFont(font)
        self.name.setStyleSheet("")
        self.name.setObjectName("name")
        self.Btn_Turn_Left = QtWidgets.QPushButton(Client)
        self.Btn_Turn_Left.setGeometry(QtCore.QRect(10, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Turn_Left.setFont(font)
        self.Btn_Turn_Left.setStyleSheet("")
        self.Btn_Turn_Left.setObjectName("Btn_Turn_Left")
        self.Btn_BackWard = QtWidgets.QPushButton(Client)
        self.Btn_BackWard.setGeometry(QtCore.QRect(120, 560, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_BackWard.setFont(font)
        self.Btn_BackWard.setStyleSheet("")
        self.Btn_BackWard.setObjectName("Btn_BackWard")
        self.Btn_Turn_Right = QtWidgets.QPushButton(Client)
        self.Btn_Turn_Right.setGeometry(QtCore.QRect(230, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Turn_Right.setFont(font)
        self.Btn_Turn_Right.setStyleSheet("")
        self.Btn_Turn_Right.setObjectName("Btn_Turn_Right")
        self.Btn_Video = QtWidgets.QPushButton(Client)
        self.Btn_Video.setGeometry(QtCore.QRect(230, 380, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Video.setFont(font)
        self.Btn_Video.setStyleSheet("")
        self.Btn_Video.setObjectName("Btn_Video")
        self.label_Video = QtWidgets.QLabel(Client)
        self.label_Video.setGeometry(QtCore.QRect(1, 42, 400, 300))
        self.label_Video.setText("")
        self.label_Video.setObjectName("label_Video")
        self.Btn_Down = QtWidgets.QPushButton(Client)
        self.Btn_Down.setGeometry(QtCore.QRect(510, 490, 75, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Down.setFont(font)
        self.Btn_Down.setStyleSheet("")
        self.Btn_Down.setObjectName("Btn_Down")
        self.Btn_Left = QtWidgets.QPushButton(Client)
        self.Btn_Left.setGeometry(QtCore.QRect(440, 460, 75, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Left.setFont(font)
        self.Btn_Left.setStyleSheet("")
        self.Btn_Left.setObjectName("Btn_Left")
        self.Btn_Home = QtWidgets.QPushButton(Client)
        self.Btn_Home.setGeometry(QtCore.QRect(510, 460, 75, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Home.setFont(font)
        self.Btn_Home.setStyleSheet("")
        self.Btn_Home.setObjectName("Btn_Home")
        self.Btn_Up = QtWidgets.QPushButton(Client)
        self.Btn_Up.setGeometry(QtCore.QRect(510, 430, 75, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Up.setFont(font)
        self.Btn_Up.setStyleSheet("")
        self.Btn_Up.setObjectName("Btn_Up")
        self.Btn_Right = QtWidgets.QPushButton(Client)
        self.Btn_Right.setGeometry(QtCore.QRect(580, 460, 75, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Right.setFont(font)
        self.Btn_Right.setStyleSheet("")
        self.Btn_Right.setObjectName("Btn_Right")
        self.Window_Close = QtWidgets.QPushButton(Client)
        self.Window_Close.setGeometry(QtCore.QRect(710, 1, 50, 40))
        self.Window_Close.setObjectName("Window_Close")
        self.IP = QtWidgets.QLineEdit(Client)
        self.IP.setGeometry(QtCore.QRect(10, 380, 101, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.IP.setFont(font)
        self.IP.setStyleSheet("")
        self.IP.setObjectName("IP")
        self.Btn_Connect = QtWidgets.QPushButton(Client)
        self.Btn_Connect.setGeometry(QtCore.QRect(120, 380, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Connect.setFont(font)
        self.Btn_Connect.setObjectName("Btn_Connect")
        self.checkBox_Led1 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led1.setGeometry(QtCore.QRect(420, 120, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led1.setFont(font)
        self.checkBox_Led1.setObjectName("checkBox_Led1")
        self.label_Servo2 = QtWidgets.QLabel(Client)
        self.label_Servo2.setGeometry(QtCore.QRect(710, 470, 41, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(14)
        self.label_Servo2.setFont(font)
        self.label_Servo2.setObjectName("label_Servo2")
        self.checkBox_Led2 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led2.setGeometry(QtCore.QRect(420, 170, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led2.setFont(font)
        self.checkBox_Led2.setObjectName("checkBox_Led2")
        self.checkBox_Led3 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led3.setGeometry(QtCore.QRect(420, 220, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led3.setFont(font)
        self.checkBox_Led3.setObjectName("checkBox_Led3")
        self.checkBox_Led4 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led4.setGeometry(QtCore.QRect(420, 270, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led4.setFont(font)
        self.checkBox_Led4.setObjectName("checkBox_Led4")
        self.checkBox_Led5 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led5.setGeometry(QtCore.QRect(530, 120, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led5.setFont(font)
        self.checkBox_Led5.setObjectName("checkBox_Led5")
        self.checkBox_Led6 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led6.setGeometry(QtCore.QRect(530, 170, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led6.setFont(font)
        self.checkBox_Led6.setObjectName("checkBox_Led6")
        self.checkBox_Led7 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led7.setGeometry(QtCore.QRect(530, 220, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led7.setFont(font)
        self.checkBox_Led7.setObjectName("checkBox_Led7")
        self.checkBox_Led8 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led8.setGeometry(QtCore.QRect(530, 270, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led8.setFont(font)
        self.checkBox_Led8.setObjectName("checkBox_Led8")
        self.HSlider_Servo1 = QtWidgets.QSlider(Client)
        self.HSlider_Servo1.setGeometry(QtCore.QRect(470, 540, 160, 22))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.HSlider_Servo1.setFont(font)
        self.HSlider_Servo1.setStyleSheet("")
        self.HSlider_Servo1.setOrientation(QtCore.Qt.Horizontal)
        self.HSlider_Servo1.setObjectName("HSlider_Servo1")
        self.VSlider_Servo2 = QtWidgets.QSlider(Client)
        self.VSlider_Servo2.setGeometry(QtCore.QRect(680, 410, 22, 160))
        self.VSlider_Servo2.setStyleSheet("")
        self.VSlider_Servo2.setOrientation(QtCore.Qt.Vertical)
        self.VSlider_Servo2.setObjectName("VSlider_Servo2")
        self.label_Servo1 = QtWidgets.QLabel(Client)
        self.label_Servo1.setGeometry(QtCore.QRect(530, 570, 41, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(14)
        self.label_Servo1.setFont(font)
        self.label_Servo1.setObjectName("label_Servo1")
        self.checkBox_Led_Mode2 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led_Mode2.setGeometry(QtCore.QRect(640, 170, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led_Mode2.setFont(font)
        self.checkBox_Led_Mode2.setObjectName("checkBox_Led_Mode2")
        self.checkBox_Led_Mode3 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led_Mode3.setGeometry(QtCore.QRect(640, 220, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led_Mode3.setFont(font)
        self.checkBox_Led_Mode3.setObjectName("checkBox_Led_Mode3")
        self.checkBox_Led_Mode4 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led_Mode4.setGeometry(QtCore.QRect(640, 270, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led_Mode4.setFont(font)
        self.checkBox_Led_Mode4.setObjectName("checkBox_Led_Mode4")
        self.checkBox_Led_Mode1 = QtWidgets.QCheckBox(Client)
        self.checkBox_Led_Mode1.setGeometry(QtCore.QRect(640, 120, 91, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.checkBox_Led_Mode1.setFont(font)
        self.checkBox_Led_Mode1.setObjectName("checkBox_Led_Mode1")
        self.Color_R = QtWidgets.QLineEdit(Client)
        self.Color_R.setGeometry(QtCore.QRect(560, 90, 30, 20))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Color_R.setFont(font)
        self.Color_R.setObjectName("Color_R")
        self.Color_G = QtWidgets.QLineEdit(Client)
        self.Color_G.setGeometry(QtCore.QRect(630, 90, 30, 20))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Color_G.setFont(font)
        self.Color_G.setObjectName("Color_G")
        self.Color_B = QtWidgets.QLineEdit(Client)
        self.Color_B.setGeometry(QtCore.QRect(700, 90, 30, 20))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Color_B.setFont(font)
        self.Color_B.setObjectName("Color_B")
        self.HSlider_FineServo2 = QtWidgets.QSlider(Client)
        self.HSlider_FineServo2.setGeometry(QtCore.QRect(480, 380, 160, 22))
        self.HSlider_FineServo2.setOrientation(QtCore.Qt.Horizontal)
        self.HSlider_FineServo2.setObjectName("HSlider_FineServo2")
        self.HSlider_FineServo1 = QtWidgets.QSlider(Client)
        self.HSlider_FineServo1.setGeometry(QtCore.QRect(480, 330, 160, 22))
        self.HSlider_FineServo1.setOrientation(QtCore.Qt.Horizontal)
        self.HSlider_FineServo1.setObjectName("HSlider_FineServo1")
        self.label_FineServo1 = QtWidgets.QLabel(Client)
        self.label_FineServo1.setGeometry(QtCore.QRect(650, 330, 41, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(14)
        self.label_FineServo1.setFont(font)
        self.label_FineServo1.setObjectName("label_FineServo1")
        self.label_FineServo2 = QtWidgets.QLabel(Client)
        self.label_FineServo2.setGeometry(QtCore.QRect(650, 370, 41, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(14)
        self.label_FineServo2.setFont(font)
        self.label_FineServo2.setObjectName("label_FineServo2")
        self.Window_Min = QtWidgets.QPushButton(Client)
        self.Window_Min.setGeometry(QtCore.QRect(660, 1, 50, 40))
        self.Window_Min.setObjectName("Window_Min")
        self.R = QtWidgets.QLabel(Client)
        self.R.setGeometry(QtCore.QRect(530, 90, 16, 20))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.R.setFont(font)
        self.R.setObjectName("R")
        self.G = QtWidgets.QLabel(Client)
        self.G.setGeometry(QtCore.QRect(600, 90, 16, 20))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.G.setFont(font)
        self.G.setObjectName("G")
        self.B = QtWidgets.QLabel(Client)
        self.B.setGeometry(QtCore.QRect(670, 90, 16, 20))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.B.setFont(font)
        self.B.setObjectName("B")
        self.Led_Module = QtWidgets.QLabel(Client)
        self.Led_Module.setGeometry(QtCore.QRect(410, 90, 111, 25))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Led_Module.setFont(font)
        self.Led_Module.setObjectName("Led_Module")
        self.Servo1 = QtWidgets.QLabel(Client)
        self.Servo1.setGeometry(QtCore.QRect(420, 330, 54, 20))
        self.Servo1.setObjectName("Servo1")
        self.Servo2 = QtWidgets.QLabel(Client)
        self.Servo2.setGeometry(QtCore.QRect(420, 380, 54, 20))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Servo2.setFont(font)
        self.Servo2.setObjectName("Servo2")
        self.progress_Power = QtWidgets.QProgressBar(Client)
        self.progress_Power.setGeometry(QtCore.QRect(20, 560, 70, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.progress_Power.setFont(font)
        self.progress_Power.setStyleSheet("QProgressBar {\n"
"border: 2px solid grey;\n"
"border-radius: 5px;\n"
"background-color: #FFFFFF;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"background-color:#696969;\n"
"width: 20px;\n"
"}\n"
"\n"
"QProgressBar {\n"
"text-align: center; \n"
"color: rgb(152,251,152);\n"
"}\n"
"")
        self.progress_Power.setProperty("value", 0)
        self.progress_Power.setObjectName("progress_Power")
        self.Btn_Buzzer = QtWidgets.QPushButton(Client)
        self.Btn_Buzzer.setGeometry(QtCore.QRect(120, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Buzzer.setFont(font)
        self.Btn_Buzzer.setObjectName("Btn_Buzzer")
        self.Btn_Mode1 = QtWidgets.QRadioButton(Client)
        self.Btn_Mode1.setGeometry(QtCore.QRect(335, 410, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Mode1.setFont(font)
        self.Btn_Mode1.setObjectName("Btn_Mode1")
        self.Btn_Mode2 = QtWidgets.QRadioButton(Client)
        self.Btn_Mode2.setGeometry(QtCore.QRect(335, 460, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Mode2.setFont(font)
        self.Btn_Mode2.setObjectName("Btn_Mode2")
        self.Btn_Mode3 = QtWidgets.QRadioButton(Client)
        self.Btn_Mode3.setGeometry(QtCore.QRect(335, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Mode3.setFont(font)
        self.Btn_Mode3.setObjectName("Btn_Mode3")
        self.Btn_Mode4 = QtWidgets.QRadioButton(Client)
        self.Btn_Mode4.setGeometry(QtCore.QRect(335, 560, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Mode4.setFont(font)
        self.Btn_Mode4.setObjectName("Btn_Mode4")
        self.Btn_Tracking_Faces = QtWidgets.QPushButton(Client)
        self.Btn_Tracking_Faces.setGeometry(QtCore.QRect(230, 460, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Tracking_Faces.setFont(font)
        self.Btn_Tracking_Faces.setStyleSheet("")
        self.Btn_Tracking_Faces.setObjectName("Btn_Tracking_Faces")
        self.Ultrasonic = QtWidgets.QPushButton(Client)
        self.Ultrasonic.setGeometry(QtCore.QRect(400, 41, 180, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Ultrasonic.setFont(font)
        self.Ultrasonic.setObjectName("Ultrasonic")
        self.Light = QtWidgets.QPushButton(Client)
        self.Light.setGeometry(QtCore.QRect(580, 41, 180, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Light.setFont(font)
        self.Light.setObjectName("Light")

        self.retranslateUi(Client)
        QtCore.QMetaObject.connectSlotsByName(Client)

    def retranslateUi(self, Client):
        _translate = QtCore.QCoreApplication.translate
        Client.setWindowTitle(_translate("Client", "freenove"))
        self.Btn_ForWard.setText(_translate("Client", "ForWard"))
        self.name.setText(_translate("Client", "Freenove"))
        self.Btn_Turn_Left.setText(_translate("Client", "Turn Left"))
        self.Btn_BackWard.setText(_translate("Client", "BackWard"))
        self.Btn_Turn_Right.setText(_translate("Client", "Turn Right"))
        self.Btn_Video.setText(_translate("Client", "Open Video"))
        self.Btn_Down.setText(_translate("Client", "Down"))
        self.Btn_Left.setText(_translate("Client", "Left"))
        self.Btn_Home.setText(_translate("Client", "Home"))
        self.Btn_Up.setText(_translate("Client", "Up"))
        self.Btn_Right.setText(_translate("Client", "Right"))
        self.Window_Close.setText(_translate("Client", "×"))
        self.IP.setText(_translate("Client", "IP Address"))
        self.Btn_Connect.setText(_translate("Client", "Connect"))
        self.checkBox_Led1.setText(_translate("Client", "Led1"))
        self.label_Servo2.setText(_translate("Client", "0"))
        self.checkBox_Led2.setText(_translate("Client", "Led2"))
        self.checkBox_Led3.setText(_translate("Client", "Led3"))
        self.checkBox_Led4.setText(_translate("Client", "Led4"))
        self.checkBox_Led5.setText(_translate("Client", "Led5"))
        self.checkBox_Led6.setText(_translate("Client", "Led6"))
        self.checkBox_Led7.setText(_translate("Client", "Led7"))
        self.checkBox_Led8.setText(_translate("Client", "Led8"))
        self.label_Servo1.setText(_translate("Client", "90"))
        self.checkBox_Led_Mode2.setText(_translate("Client", "Led_Mode2"))
        self.checkBox_Led_Mode3.setText(_translate("Client", "Led_Mode3"))
        self.checkBox_Led_Mode4.setText(_translate("Client", "Led_Mode4"))
        self.checkBox_Led_Mode1.setText(_translate("Client", "Led_Mode1"))
        self.Color_R.setText(_translate("Client", "255"))
        self.Color_G.setText(_translate("Client", "0"))
        self.Color_B.setText(_translate("Client", "0"))
        self.label_FineServo1.setText(_translate("Client", "0"))
        self.label_FineServo2.setText(_translate("Client", "0"))
        self.Window_Min.setText(_translate("Client", "-"))
        self.R.setText(_translate("Client", "R"))
        self.G.setText(_translate("Client", "G"))
        self.B.setText(_translate("Client", "B"))
        self.Led_Module.setText(_translate("Client", "Led Module"))
        self.Servo1.setText(_translate("Client", "Servo 1"))
        self.Servo2.setText(_translate("Client", "Servo 2"))
        self.Btn_Buzzer.setText(_translate("Client", "Buzzer"))
        self.Btn_Mode1.setText(_translate("Client", "M-Free"))
        self.Btn_Mode2.setText(_translate("Client", "M-Light"))
        self.Btn_Mode3.setText(_translate("Client", "M-Sonic"))
        self.Btn_Mode4.setText(_translate("Client", "M-Line"))
        self.Btn_Tracking_Faces.setText(_translate("Client", "Tracing-On"))
        self.Ultrasonic.setText(_translate("Client", "Ultrasonic"))
        self.Light.setText(_translate("Client", "Light"))

