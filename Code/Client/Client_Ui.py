# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Freenove/Desktop/test/qss/Client_Ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Client(object):
    def setupUi(self, Client):
        Client.setObjectName(_fromUtf8("Client"))
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
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(14)
        Client.setFont(font)
        Client.setStyleSheet(_fromUtf8("QWidget{\n"
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
""))
        self.Btn_ForWard = QtGui.QPushButton(Client)
        self.Btn_ForWard.setGeometry(QtCore.QRect(120, 450, 90, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Btn_ForWard.setFont(font)
        self.Btn_ForWard.setStyleSheet(_fromUtf8(""))
        self.Btn_ForWard.setObjectName(_fromUtf8("Btn_ForWard"))
        self.name = QtGui.QLabel(Client)
        self.name.setGeometry(QtCore.QRect(0, 1, 660, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setStyleSheet(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.Btn_Turn_Left = QtGui.QPushButton(Client)
        self.Btn_Turn_Left.setGeometry(QtCore.QRect(10, 500, 90, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Btn_Turn_Left.setFont(font)
        self.Btn_Turn_Left.setStyleSheet(_fromUtf8(""))
        self.Btn_Turn_Left.setObjectName(_fromUtf8("Btn_Turn_Left"))
        self.Btn_BackWard = QtGui.QPushButton(Client)
        self.Btn_BackWard.setGeometry(QtCore.QRect(120, 550, 90, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Btn_BackWard.setFont(font)
        self.Btn_BackWard.setStyleSheet(_fromUtf8(""))
        self.Btn_BackWard.setObjectName(_fromUtf8("Btn_BackWard"))
        self.Btn_Turn_Right = QtGui.QPushButton(Client)
        self.Btn_Turn_Right.setGeometry(QtCore.QRect(240, 500, 90, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Btn_Turn_Right.setFont(font)
        self.Btn_Turn_Right.setStyleSheet(_fromUtf8(""))
        self.Btn_Turn_Right.setObjectName(_fromUtf8("Btn_Turn_Right"))
        self.Btn_Video = QtGui.QPushButton(Client)
        self.Btn_Video.setGeometry(QtCore.QRect(240, 380, 90, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Btn_Video.setFont(font)
        self.Btn_Video.setStyleSheet(_fromUtf8(""))
        self.Btn_Video.setObjectName(_fromUtf8("Btn_Video"))
        self.label_Video = QtGui.QLabel(Client)
        self.label_Video.setGeometry(QtCore.QRect(1, 42, 400, 300))
        self.label_Video.setText(_fromUtf8(""))
        self.label_Video.setObjectName(_fromUtf8("label_Video"))
        self.Btn_Down = QtGui.QPushButton(Client)
        self.Btn_Down.setGeometry(QtCore.QRect(510, 480, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Down.setFont(font)
        self.Btn_Down.setStyleSheet(_fromUtf8(""))
        self.Btn_Down.setObjectName(_fromUtf8("Btn_Down"))
        self.Btn_Left = QtGui.QPushButton(Client)
        self.Btn_Left.setGeometry(QtCore.QRect(440, 450, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Left.setFont(font)
        self.Btn_Left.setStyleSheet(_fromUtf8(""))
        self.Btn_Left.setObjectName(_fromUtf8("Btn_Left"))
        self.Btn_Home = QtGui.QPushButton(Client)
        self.Btn_Home.setGeometry(QtCore.QRect(510, 450, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Home.setFont(font)
        self.Btn_Home.setStyleSheet(_fromUtf8(""))
        self.Btn_Home.setObjectName(_fromUtf8("Btn_Home"))
        self.Btn_Up = QtGui.QPushButton(Client)
        self.Btn_Up.setGeometry(QtCore.QRect(510, 420, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Up.setFont(font)
        self.Btn_Up.setStyleSheet(_fromUtf8(""))
        self.Btn_Up.setObjectName(_fromUtf8("Btn_Up"))
        self.Btn_Right = QtGui.QPushButton(Client)
        self.Btn_Right.setGeometry(QtCore.QRect(580, 450, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Right.setFont(font)
        self.Btn_Right.setStyleSheet(_fromUtf8(""))
        self.Btn_Right.setObjectName(_fromUtf8("Btn_Right"))
        self.Window_Close = QtGui.QPushButton(Client)
        self.Window_Close.setGeometry(QtCore.QRect(710, 1, 50, 40))
        self.Window_Close.setObjectName(_fromUtf8("Window_Close"))
        self.IP = QtGui.QLineEdit(Client)
        self.IP.setGeometry(QtCore.QRect(10, 380, 101, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.IP.setFont(font)
        self.IP.setStyleSheet(_fromUtf8(""))
        self.IP.setObjectName(_fromUtf8("IP"))
        self.Btn_Connect = QtGui.QPushButton(Client)
        self.Btn_Connect.setGeometry(QtCore.QRect(120, 380, 90, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Btn_Connect.setFont(font)
        self.Btn_Connect.setObjectName(_fromUtf8("Btn_Connect"))
        self.checkBox_Led1 = QtGui.QCheckBox(Client)
        self.checkBox_Led1.setGeometry(QtCore.QRect(420, 120, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led1.setFont(font)
        self.checkBox_Led1.setObjectName(_fromUtf8("checkBox_Led1"))
        self.label_Servo2 = QtGui.QLabel(Client)
        self.label_Servo2.setGeometry(QtCore.QRect(710, 460, 41, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(14)
        self.label_Servo2.setFont(font)
        self.label_Servo2.setObjectName(_fromUtf8("label_Servo2"))
        self.checkBox_Led2 = QtGui.QCheckBox(Client)
        self.checkBox_Led2.setGeometry(QtCore.QRect(420, 170, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led2.setFont(font)
        self.checkBox_Led2.setObjectName(_fromUtf8("checkBox_Led2"))
        self.checkBox_Led3 = QtGui.QCheckBox(Client)
        self.checkBox_Led3.setGeometry(QtCore.QRect(420, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led3.setFont(font)
        self.checkBox_Led3.setObjectName(_fromUtf8("checkBox_Led3"))
        self.checkBox_Led4 = QtGui.QCheckBox(Client)
        self.checkBox_Led4.setGeometry(QtCore.QRect(420, 270, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led4.setFont(font)
        self.checkBox_Led4.setObjectName(_fromUtf8("checkBox_Led4"))
        self.checkBox_Led5 = QtGui.QCheckBox(Client)
        self.checkBox_Led5.setGeometry(QtCore.QRect(530, 120, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led5.setFont(font)
        self.checkBox_Led5.setObjectName(_fromUtf8("checkBox_Led5"))
        self.checkBox_Led6 = QtGui.QCheckBox(Client)
        self.checkBox_Led6.setGeometry(QtCore.QRect(530, 170, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led6.setFont(font)
        self.checkBox_Led6.setObjectName(_fromUtf8("checkBox_Led6"))
        self.checkBox_Led7 = QtGui.QCheckBox(Client)
        self.checkBox_Led7.setGeometry(QtCore.QRect(530, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led7.setFont(font)
        self.checkBox_Led7.setObjectName(_fromUtf8("checkBox_Led7"))
        self.checkBox_Led8 = QtGui.QCheckBox(Client)
        self.checkBox_Led8.setGeometry(QtCore.QRect(530, 270, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led8.setFont(font)
        self.checkBox_Led8.setObjectName(_fromUtf8("checkBox_Led8"))
        self.HSlider_Servo1 = QtGui.QSlider(Client)
        self.HSlider_Servo1.setGeometry(QtCore.QRect(470, 530, 160, 22))
        self.HSlider_Servo1.setStyleSheet(_fromUtf8(""))
        self.HSlider_Servo1.setOrientation(QtCore.Qt.Horizontal)
        self.HSlider_Servo1.setObjectName(_fromUtf8("HSlider_Servo1"))
        self.VSlider_Servo2 = QtGui.QSlider(Client)
        self.VSlider_Servo2.setGeometry(QtCore.QRect(680, 400, 22, 160))
        self.VSlider_Servo2.setStyleSheet(_fromUtf8(""))
        self.VSlider_Servo2.setOrientation(QtCore.Qt.Vertical)
        self.VSlider_Servo2.setObjectName(_fromUtf8("VSlider_Servo2"))
        self.label_Servo1 = QtGui.QLabel(Client)
        self.label_Servo1.setGeometry(QtCore.QRect(530, 560, 41, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(14)
        self.label_Servo1.setFont(font)
        self.label_Servo1.setObjectName(_fromUtf8("label_Servo1"))
        self.checkBox_Led_Mode2 = QtGui.QCheckBox(Client)
        self.checkBox_Led_Mode2.setGeometry(QtCore.QRect(640, 170, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led_Mode2.setFont(font)
        self.checkBox_Led_Mode2.setObjectName(_fromUtf8("checkBox_Led_Mode2"))
        self.checkBox_Led_Mode3 = QtGui.QCheckBox(Client)
        self.checkBox_Led_Mode3.setGeometry(QtCore.QRect(640, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led_Mode3.setFont(font)
        self.checkBox_Led_Mode3.setObjectName(_fromUtf8("checkBox_Led_Mode3"))
        self.checkBox_Led_Mode4 = QtGui.QCheckBox(Client)
        self.checkBox_Led_Mode4.setGeometry(QtCore.QRect(640, 270, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led_Mode4.setFont(font)
        self.checkBox_Led_Mode4.setObjectName(_fromUtf8("checkBox_Led_Mode4"))
        self.checkBox_Led_Mode1 = QtGui.QCheckBox(Client)
        self.checkBox_Led_Mode1.setGeometry(QtCore.QRect(640, 120, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_Led_Mode1.setFont(font)
        self.checkBox_Led_Mode1.setObjectName(_fromUtf8("checkBox_Led_Mode1"))
        self.Color_R = QtGui.QLineEdit(Client)
        self.Color_R.setGeometry(QtCore.QRect(560, 90, 30, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Color_R.setFont(font)
        self.Color_R.setObjectName(_fromUtf8("Color_R"))
        self.Color_G = QtGui.QLineEdit(Client)
        self.Color_G.setGeometry(QtCore.QRect(630, 90, 30, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Color_G.setFont(font)
        self.Color_G.setObjectName(_fromUtf8("Color_G"))
        self.Color_B = QtGui.QLineEdit(Client)
        self.Color_B.setGeometry(QtCore.QRect(700, 90, 30, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Color_B.setFont(font)
        self.Color_B.setObjectName(_fromUtf8("Color_B"))
        self.HSlider_FineServo2 = QtGui.QSlider(Client)
        self.HSlider_FineServo2.setGeometry(QtCore.QRect(480, 370, 160, 22))
        self.HSlider_FineServo2.setOrientation(QtCore.Qt.Horizontal)
        self.HSlider_FineServo2.setObjectName(_fromUtf8("HSlider_FineServo2"))
        self.HSlider_FineServo1 = QtGui.QSlider(Client)
        self.HSlider_FineServo1.setGeometry(QtCore.QRect(480, 320, 160, 22))
        self.HSlider_FineServo1.setOrientation(QtCore.Qt.Horizontal)
        self.HSlider_FineServo1.setObjectName(_fromUtf8("HSlider_FineServo1"))
        self.label_FineServo1 = QtGui.QLabel(Client)
        self.label_FineServo1.setGeometry(QtCore.QRect(650, 320, 41, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(14)
        self.label_FineServo1.setFont(font)
        self.label_FineServo1.setObjectName(_fromUtf8("label_FineServo1"))
        self.label_FineServo2 = QtGui.QLabel(Client)
        self.label_FineServo2.setGeometry(QtCore.QRect(650, 360, 41, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(14)
        self.label_FineServo2.setFont(font)
        self.label_FineServo2.setObjectName(_fromUtf8("label_FineServo2"))
        self.Window_Min = QtGui.QPushButton(Client)
        self.Window_Min.setGeometry(QtCore.QRect(660, 1, 50, 40))
        self.Window_Min.setObjectName(_fromUtf8("Window_Min"))
        self.R = QtGui.QLabel(Client)
        self.R.setGeometry(QtCore.QRect(530, 90, 16, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.R.setFont(font)
        self.R.setObjectName(_fromUtf8("R"))
        self.G = QtGui.QLabel(Client)
        self.G.setGeometry(QtCore.QRect(600, 90, 16, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.G.setFont(font)
        self.G.setObjectName(_fromUtf8("G"))
        self.B = QtGui.QLabel(Client)
        self.B.setGeometry(QtCore.QRect(670, 90, 16, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.B.setFont(font)
        self.B.setObjectName(_fromUtf8("B"))
        self.Led_Module = QtGui.QLabel(Client)
        self.Led_Module.setGeometry(QtCore.QRect(410, 90, 111, 25))
        self.Led_Module.setObjectName(_fromUtf8("Led_Module"))
        self.Servo1 = QtGui.QLabel(Client)
        self.Servo1.setGeometry(QtCore.QRect(420, 320, 54, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Servo1.setFont(font)
        self.Servo1.setObjectName(_fromUtf8("Servo1"))
        self.Servo2 = QtGui.QLabel(Client)
        self.Servo2.setGeometry(QtCore.QRect(420, 370, 54, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(10)
        self.Servo2.setFont(font)
        self.Servo2.setObjectName(_fromUtf8("Servo2"))
        self.progress_Power = QtGui.QProgressBar(Client)
        self.progress_Power.setGeometry(QtCore.QRect(20, 550, 70, 30))
        self.progress_Power.setStyleSheet(_fromUtf8("QProgressBar {\n"
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
""))
        self.progress_Power.setProperty("value", 0)
        self.progress_Power.setObjectName(_fromUtf8("progress_Power"))
        self.Btn_Buzzer = QtGui.QPushButton(Client)
        self.Btn_Buzzer.setGeometry(QtCore.QRect(120, 500, 90, 30))
        self.Btn_Buzzer.setObjectName(_fromUtf8("Btn_Buzzer"))
        self.Ultrasonic = QtGui.QPushButton(Client)
        self.Ultrasonic.setGeometry(QtCore.QRect(401, 41, 180, 30))
        self.Ultrasonic.setObjectName(_fromUtf8("Ultrasonic"))
        self.Light = QtGui.QPushButton(Client)
        self.Light.setGeometry(QtCore.QRect(581, 41, 179, 30))
        self.Light.setObjectName(_fromUtf8("Light"))
        self.Btn_Mode1 = QtGui.QRadioButton(Client)
        self.Btn_Mode1.setGeometry(QtCore.QRect(340, 400, 90, 30))
        self.Btn_Mode1.setObjectName(_fromUtf8("Btn_Mode1"))
        self.Btn_Mode2 = QtGui.QRadioButton(Client)
        self.Btn_Mode2.setGeometry(QtCore.QRect(340, 450, 90, 30))
        self.Btn_Mode2.setObjectName(_fromUtf8("Btn_Mode2"))
        self.Btn_Mode3 = QtGui.QRadioButton(Client)
        self.Btn_Mode3.setGeometry(QtCore.QRect(340, 500, 90, 30))
        self.Btn_Mode3.setObjectName(_fromUtf8("Btn_Mode3"))
        self.Btn_Mode4 = QtGui.QRadioButton(Client)
        self.Btn_Mode4.setGeometry(QtCore.QRect(340, 550, 90, 30))
        self.Btn_Mode4.setObjectName(_fromUtf8("Btn_Mode4"))

        self.retranslateUi(Client)
        QtCore.QMetaObject.connectSlotsByName(Client)

    def retranslateUi(self, Client):
        Client.setWindowTitle(_translate("Client", "freenove", None))
        self.Btn_ForWard.setText(_translate("Client", "ForWard", None))
        self.name.setText(_translate("Client", "Freenove", None))
        self.Btn_Turn_Left.setText(_translate("Client", "Turn Left", None))
        self.Btn_BackWard.setText(_translate("Client", "BackWard", None))
        self.Btn_Turn_Right.setText(_translate("Client", "Turn Right", None))
        self.Btn_Video.setText(_translate("Client", "Open Video", None))
        self.Btn_Down.setText(_translate("Client", "Down", None))
        self.Btn_Left.setText(_translate("Client", "Left", None))
        self.Btn_Home.setText(_translate("Client", "Home", None))
        self.Btn_Up.setText(_translate("Client", "Up", None))
        self.Btn_Right.setText(_translate("Client", "Right", None))
        self.Window_Close.setText(_translate("Client", "×", None))
        self.IP.setText(_translate("Client", "192.168.1.118", None))
        self.Btn_Connect.setText(_translate("Client", "Connect", None))
        self.checkBox_Led1.setText(_translate("Client", "Led1", None))
        self.label_Servo2.setText(_translate("Client", "0", None))
        self.checkBox_Led2.setText(_translate("Client", "Led2", None))
        self.checkBox_Led3.setText(_translate("Client", "Led3", None))
        self.checkBox_Led4.setText(_translate("Client", "Led4", None))
        self.checkBox_Led5.setText(_translate("Client", "Led5", None))
        self.checkBox_Led6.setText(_translate("Client", "Led6", None))
        self.checkBox_Led7.setText(_translate("Client", "Led7", None))
        self.checkBox_Led8.setText(_translate("Client", "Led8", None))
        self.label_Servo1.setText(_translate("Client", "90", None))
        self.checkBox_Led_Mode2.setText(_translate("Client", "Led_Mode2", None))
        self.checkBox_Led_Mode3.setText(_translate("Client", "Led_Mode3", None))
        self.checkBox_Led_Mode4.setText(_translate("Client", "Led_Mode4", None))
        self.checkBox_Led_Mode1.setText(_translate("Client", "Led_Mode1", None))
        self.Color_R.setText(_translate("Client", "255", None))
        self.Color_G.setText(_translate("Client", "0", None))
        self.Color_B.setText(_translate("Client", "0", None))
        self.label_FineServo1.setText(_translate("Client", "0", None))
        self.label_FineServo2.setText(_translate("Client", "0", None))
        self.Window_Min.setText(_translate("Client", "-", None))
        self.R.setText(_translate("Client", "R", None))
        self.G.setText(_translate("Client", "G", None))
        self.B.setText(_translate("Client", "B", None))
        self.Led_Module.setText(_translate("Client", "Led Module", None))
        self.Servo1.setText(_translate("Client", "Servo 1", None))
        self.Servo2.setText(_translate("Client", "Servo 2", None))
        self.Btn_Buzzer.setText(_translate("Client", "Buzzer", None))
        self.Ultrasonic.setText(_translate("Client", "Ultrasonic", None))
        self.Light.setText(_translate("Client", "Light", None))
        self.Btn_Mode1.setText(_translate("Client", "M-Free", None))
        self.Btn_Mode2.setText(_translate("Client", "M-Light", None))
        self.Btn_Mode3.setText(_translate("Client", "M-Sonic", None))
        self.Btn_Mode4.setText(_translate("Client", "M-Line", None))

