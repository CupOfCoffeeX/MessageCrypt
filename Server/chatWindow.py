import sys
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMessageBox, QTabWidget
from PyQt5.QtWidgets import QGridLayout, QScrollArea, QLabel, QListView
from PyQt5.QtWidgets import QLineEdit, QComboBox, QGroupBox, QAction
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont

import socket

import time


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.centralwidget = QtWidgets.QWidget(parent)
        #connecion
        self.conn = socket.socket()
        self.connected = False
        #tab UI
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Chat Room")
        self.tabs.setTabEnabled(1,False)
        #<Chat Room>
        gridChatRoom = QGridLayout()
        self.tab2.setLayout(gridChatRoom)
        self.messageRecords = QLabel("<font color=\"#000000\">Welcome to chat room</font>", self)
        self.messageRecords.setStyleSheet("background-color: white;");
        self.messageRecords.setAlignment(QtCore.Qt.AlignTop)
        self.messageRecords.setAutoFillBackground(True);
        self.scrollRecords = QScrollArea()
        self.scrollRecords.setWidget(self.messageRecords)
        self.scrollRecords.setWidgetResizable(True)
        self.sendTo = "ALL"
        #self.sendChoice = QLabel("Send to :ALL", self)
        #self.sendComboBox = QComboBox(self)
        #self.sendComboBox.addItem("ALL")
        self.lineEdit = QLineEdit()
        self.lineEnterBtn = QPushButton("Envoyer")
        self.lineEnterBtn.clicked.connect(self.enter_btn_pressed)
        self.friendList = QListView()
        self.friendList.setWindowTitle('Room List')
        self.model = QStandardItemModel(self.friendList)
        self.friendList.setModel(self.model)
        gridChatRoom.addWidget(self.scrollRecords,0,0,1,3)
        gridChatRoom.addWidget(self.friendList,0,3,1,1)
        #gridChatRoom.addWidget(self.sendComboBox,1,0,1,1)
        #gridChatRoom.addWidget(self.sendChoice,1,2,1,1)
        gridChatRoom.addWidget(self.lineEdit,2,0,1,3)
        gridChatRoom.addWidget(self.lineEnterBtn,2,3,1,1)
        gridChatRoom.setColumnStretch(0, 9)
        gridChatRoom.setColumnStretch(1, 9)
        gridChatRoom.setColumnStretch(2, 9)
        gridChatRoom.setColumnStretch(3, 1)
        gridChatRoom.setRowStretch(0, 9)
        #</Chat Room>
        #Initialization
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.listFriend = []
        print("okok")

    def print_message(self, newMessage, textColor="#000000"):
        print('new message')
        oldText = self.messageRecords.text()
        appendText = oldText + "<br /><font color=\"" + textColor + "\">" + newMessage + "</font><font color=\"#000000\"></font>"
        self.messageRecords.setText(appendText)
        time.sleep(0.2)  # this helps the bar set to bottom, after all message already appended
        self.scrollRecords.verticalScrollBar().setValue(self.scrollRecords.verticalScrollBar().maximum())

    def enter_btn_pressed(self):
        actual_lines = self.lineEdit.text()
        if actual_lines == "":
            return
        self.print_message(actual_lines)
        self.lineEdit.clear()

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("Voullez-vous vraiment quitter ?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def addToFriendList(self, item):
        self.listFriend.append(item)
        new = QStandardItem(item)
        self.model.appendRow(new)
        #self.model.clear()

    def deleteFriend(self, name):
        compteur = 0
        for i in self.listFriend:
            if i == name:
                del self.listFriend[compteur]
            compteur += 1

        self.model.clear()
        for elem in self.listFriend:
            new = QStandardItem(elem)
            self.model.appendRow(new)