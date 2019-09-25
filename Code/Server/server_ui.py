# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Freenove/Desktop/test/qss/server_ui.ui'
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

class Ui_server_ui(object):
    def setupUi(self, server_ui):
        server_ui.setObjectName(_fromUtf8("server_ui"))
        server_ui.resize(400, 300)
        server_ui.setStyleSheet(_fromUtf8("QWidget{\n"
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
"}"))
        self.label = QtGui.QLabel(server_ui)
        self.label.setGeometry(QtCore.QRect(100, 150, 200, 42))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.Button_Server = QtGui.QPushButton(server_ui)
        self.Button_Server.setGeometry(QtCore.QRect(150, 220, 100, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(12)
        self.Button_Server.setFont(font)
        self.Button_Server.setObjectName(_fromUtf8("Button_Server"))
        self.label_2 = QtGui.QLabel(server_ui)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 301, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("3ds"))
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_Close = QtGui.QPushButton(server_ui)
        self.pushButton_Close.setGeometry(QtCore.QRect(350, 0, 50, 40))
        self.pushButton_Close.setObjectName(_fromUtf8("pushButton_Close"))
        self.pushButton_Min = QtGui.QPushButton(server_ui)
        self.pushButton_Min.setGeometry(QtCore.QRect(300, 0, 50, 40))
        self.pushButton_Min.setObjectName(_fromUtf8("pushButton_Min"))

        self.retranslateUi(server_ui)
        QtCore.QMetaObject.connectSlotsByName(server_ui)

    def retranslateUi(self, server_ui):
        server_ui.setWindowTitle(_translate("server_ui", "Form", None))
        self.label.setText(_translate("server_ui", "Server Off", None))
        self.Button_Server.setText(_translate("server_ui", "Off", None))
        self.label_2.setText(_translate("server_ui", "Freenove", None))
        self.pushButton_Close.setText(_translate("server_ui", "×", None))
        self.pushButton_Min.setText(_translate("server_ui", "-", None))

