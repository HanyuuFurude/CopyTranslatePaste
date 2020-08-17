# -*- coding: utf-8 -*-
'''
@author: HanyuuLu
@date 2020-08-17

https://hanyuulu.github.io/CopyTranslatePaste/
CopyTranslatePaste
Copyright (C) 2019
'''

import datetime
import sys
import threading
import time
import os

# from PyQt5 import *
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.QtWidgets import (
    QAction, QApplication, QCheckBox, QGraphicsRectItem, QGridLayout,
    QLabel, QMainWindow, QMenu, QMessageBox, QPushButton, QStatusBar, QSystemTrayIcon, QTextBrowser, QTextEdit, QGridLayout, QWidget
)

from utils import translate
from utils.clipboardUtils import clipboard
from utils import log

# 程序名
TITLE = "Kuro"


class MainUX(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.title = 'Kuro'
        self.wgtCanvas = QWidget()
        self.wgtCanvas.setObjectName("mainCanvas")
        self.setCentralWidget(self.wgtCanvas)
        self.autoRead = True
        self.autoWrite = True
        self.res = None  # 翻译结果储存变量
        self.text = None  # 待翻译文本储存变量
        self.webfailFlag = False
        self.timeTag = time.time()

        # 控件生成
        self.qlbInputLabel = QLabel("from")
        self.qlbInputLabel.setObjectName("inputLabel")
        self.qteInputText = QTextEdit()
        # self.qteInputText.textChanged.connect(self.bang)
        self.qlbResultLabel = QLabel("to")
        self.qlbResultLabel.setObjectName("outputLabel")
        self.qteResultText = QTextEdit()
        self.timer = QTimer(self)  # 剪切板访问定时器

        # 控件布局
        # 设置区空间布局
        # 主ui控件布局
        self.qltMainLayout = QGridLayout()
        self.qltMainLayout.setVerticalSpacing(0)
        self.qltMainLayout.addWidget(self.qlbInputLabel, 1, 0)
        self.qltMainLayout.addWidget(self.qteInputText, 0, 0, 1, 2)
        self.qltMainLayout.addWidget(self.qlbResultLabel, 1, 1)
        self.qltMainLayout.addWidget(self.qteResultText, 2, 0, 1, 2)
        self.wgtCanvas.setLayout(self.qltMainLayout)

        # 窗口置顶
        self.setWindowFlags(
            # QtCore.Qt.WindowMinimizeButtonHint |
            # QtCore.Qt.WindowMaximizeButtonHint |
            # QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.FramelessWindowHint
        )
        self.setFixedSize(200, 150)

        # Place the tray icon
        self.trayIcon = TrayIcon(self)
        self.trayIcon.show()

        # QSS
        for folder, subfolder, files in os.walk("./style"):
            styleStatement = ""
            for file in files:
                try:
                    with open(os.path.join(folder, file), 'r') as r:
                        styleStatement += r.read()
                except Exception as e:
                    QMessageBox(self, 'Error', 'qss文件读取失败', QMessageBox.Yes)
            self.setStyleSheet(styleStatement)

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 功能绑定区
        self.timer.timeout.connect(self.bang)
        self.timer.start(1000)

        self.show()
        return

    # 窗口拖拽
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.movingFlag = True
            self.movingPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(Qt.OpenHandCursor))
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.movingFlag:
            self.move(event.globalPos() - self.movingPosition)
            event.accept()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.movingFlag = False
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    # fetch the text from textOrigin
    def fetchPlainText(self):
        return self.qteInputText.toPlainText()

    # set the text to textTranslate
    def setPlainText(self, text):
        self.qteResultText.clear()
        self.qteResultText.setPlainText(text)
        return text

    def bang(self):
        text = clipboard.getText()
        if self.autoRead is False and self.fetchPlainText() != self.text:
            self.text = self.fetchPlainText()
            self.translate(self.text)
        elif text is None or text == self.res or text == self.text:
            return
        elif self.autoRead is True:
            self.text = text
            self.qteInputText.clear()
            self.qteInputText.setPlainText(self.text)
            self.translate(self.text)

    def translate(self, src):
        print(time.time())
        if src is None or src == '':
            return
        try:
            self.res = translate(src)
        except Exception as e:
            log.error(e)
            self.setPlainText('[网络出错]')
            self.webfailFlag = True
            return
        self.webfailFlag = False
        self.setPlainText(self.res)
        if self.autoWrite is True:
            clipboard.setText(self.res)
        print("translate success")


class TrayIcon(QSystemTrayIcon):
    '''
    # The component of the tray icon
    '''

    def __init__(self, uiHandle):
        QSystemTrayIcon.__init__(self)
        super().__init__(self)
        self.uiHandle = uiHandle
        self.icon = QtGui.QIcon("ico.ico")
        self.initMenu()

    def initMenu(self):
        '''
        # draw the menu for tray icon
        '''
        self.menu = QMenu()
        self.actShow = QAction(
            "显示、隐藏窗体", self,
            triggered=self.uiShowHide)
        self.actReadFromClipboard = QAction(
            "从剪切板读取", self,
            triggered=self.switchRead)
        self.actWriteToClipboard = QAction(
            "写回剪切板", self,
            triggered=self.switchWrite)
        self.actQuit = QAction(
            "退出", self,
            triggered=self.quit)

        self.menu.addAction(self.actShow)
        self.menu.addAction(self.actReadFromClipboard)
        self.menu.addAction(self.actWriteToClipboard)
        self.menu.addAction(self.actQuit)
        self.setContextMenu(self.menu)
        # self.activated.connect(self.iconClied)
        # # 把鼠标点击图标的信号和槽连接
        # self.messageClicked.connect(self.exampleMessage)
        # 把鼠标点击弹出消息的信号和槽连接
        self.setIcon(self.icon)

        # 设置图标

    # def exampleMessage(self):
    #     self.showMessage("Hint", "Message trigged", self.icon)

    def showMessage(self, title, msg, icon):
        return super().showMessage(title, msg, icon)

    def switchRead(self):
        self.uiHandle.autoRead = not self.uiHandle.autoRead
        self.showMessage(TITLE, "已%s读取剪切板功能" %
                         ("开启" if self.uiHandle.autoRead else "关闭"), self.icon)

    def switchWrite(self):
        self.uiHandle.autoWrite = not self.uiHandle.autoWrite
        self.showMessage(TITLE, "已%s写回剪切板功能" %
                         ("开启" if self.uiHandle.autoWrite else "关闭"), self.icon)

    def quit(self):
        self.uiHandle.close()

    def uiShowHide(self):
        if self.uiHandle.isVisible():
            self.uiHandle.hide()
        else:
            self.uiHandle.show()

    # def iconClied(self, reason):
    #     "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
    #     if reason == 2 or reason == 3:
    #         pw = self.uiHandle
    #         if pw.isVisible():
    #             pw.hide()
    #         else:
    #             pw.show()
    #     # print(reason)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainUX = MainUX()
    sys.exit(app.exec_())
