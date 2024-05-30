# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Freenove\Desktop\树莓派四轮车项目\四轮车（python3+pyqt5）代码\server_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_server_ui(object):
    def setupUi(self, server_ui):
        server_ui.setObjectName("server_ui")
        server_ui.resize(400, 300)
        font = QtGui.QFont()
        font.setFamily("3ds")
        server_ui.setFont(font)
        server_ui.setStyleSheet("QWidget{\n"
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
"border:1px solid #484848;\n"
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
"}")
        self.label = QtWidgets.QLabel(server_ui)
        self.label.setGeometry(QtCore.QRect(100, 150, 200, 42))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Button_Server = QtWidgets.QPushButton(server_ui)
        self.Button_Server.setGeometry(QtCore.QRect(150, 220, 100, 40))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(12)
        self.Button_Server.setFont(font)
        self.Button_Server.setObjectName("Button_Server")
        self.label_2 = QtWidgets.QLabel(server_ui)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 301, 41))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.pushButton_Close = QtWidgets.QPushButton(server_ui)
        self.pushButton_Close.setGeometry(QtCore.QRect(350, 0, 50, 40))
        font = QtGui.QFont()
        font.setFamily("3ds")
        self.pushButton_Close.setFont(font)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.pushButton_Min = QtWidgets.QPushButton(server_ui)
        self.pushButton_Min.setGeometry(QtCore.QRect(300, 0, 50, 40))
        font = QtGui.QFont()
        font.setFamily("3ds")
        self.pushButton_Min.setFont(font)
        self.pushButton_Min.setObjectName("pushButton_Min")

        self.retranslateUi(server_ui)
        QtCore.QMetaObject.connectSlotsByName(server_ui)

    def retranslateUi(self, server_ui):
        _translate = QtCore.QCoreApplication.translate
        server_ui.setWindowTitle(_translate("server_ui", "Form"))
        self.label.setText(_translate("server_ui", "Server Off"))
        self.Button_Server.setText(_translate("server_ui", "Off"))
        self.label_2.setText(_translate("server_ui", "freenove"))
        self.pushButton_Close.setText(_translate("server_ui", "×"))
        self.pushButton_Min.setText(_translate("server_ui", "-"))

