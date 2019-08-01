'''
@author: Hanyuu Furude
Copyright (C) 2019
'''
import datetime
import sys
import threading
import time

# from PyQt5 import *
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QGraphicsRectItem,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QSystemTrayIcon,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget
)

import translate

# 程序名
TITLE = "Kuro"


class MainUX(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.title = 'Kuro'
        self.wgtCanvas = QWidget()
        self.setCentralWidget(self.wgtCanvas)
        self.autoRead = True
        self.autoWrite = True
        self.res = None  # 翻译结果储存变量
        self.text = None  # 待翻译文本储存变量

        # 控件生成
        # self.qlbAutoRead = QLabel("自动读取内存文本")
        # self.qcbAutoRead = QCheckBox()
        # self.qcbAutoRead.setCheckState(Qt.Checked)
        # self.qlbAutoCopy = QLabel("自动将结果写入剪切板")
        # self.qcbAutoCopy = QCheckBox()
        # self.qcbAutoCopy.setCheckState(Qt.Checked)
        self.qlbInputLabel = QLabel("Input box")
        self.qteInputText = QTextEdit()
        self.qlbResultLabel = QLabel("result")
        self.qteResultText = QTextEdit()
        # self.btnExit = QPushButton("退出")
        self.timer = QTimer(self)  # 剪切板访问定时器

        # 控件布局
        # 设置区空间布局
        # self.wgtSettingArea = QWidget()
        # self.QltSettingLayout = QGridLayout()
        # self.QltSettingLayout.addWidget(self.qlbAutoRead, 0, 1)
        # self.QltSettingLayout.addWidget(self.qcbAutoRead, 0, 0)
        # self.QltSettingLayout.addWidget(self.qlbAutoCopy, 1, 1)
        # self.QltSettingLayout.addWidget(self.qcbAutoCopy, 1, 0)
        # self.wgtSettingArea.setLayout(self.QltSettingLayout)
        # 主ui控件布局
        self.qltMainLayout = QVBoxLayout()
        # self.qltMainLayout.addWidget(self.wgtSettingArea)
        # self.qltMainLayout.addWidget(self.qlbAutoRead)
        # self.qltMainLayout.addWidget(self.qcbAutoRead)
        # self.qltMainLayout.addWidget(self.qlbAutoCopy)
        # self.qltMainLayout.addWidget(self.qcbAutoCopy)
        self.qltMainLayout.addWidget(self.qlbInputLabel)
        self.qltMainLayout.addWidget(self.qteInputText)
        self.qltMainLayout.addWidget(self.qlbResultLabel)
        self.qltMainLayout.addWidget(self.qteResultText)
        # self.qltMainLayout.addWidget(self.btnExit)
        self.wgtCanvas.setLayout(self.qltMainLayout)
        self.setWindowTitle(self.title)

        # 窗口置顶
        self.setWindowFlags(
            # QtCore.Qt.WindowMinimizeButtonHint |
            # QtCore.Qt.WindowMaximizeButtonHint |
            # QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.CustomizeWindowHint
        )
        self.setFixedSize(self.width(), self.height())

        # Place the tray icon
        self.trayIcon = TrayIcon(self)
        self.trayIcon.show()

        # QSS
        try:
            with open('ui.qss', 'r') as r:
                styleSheet = r.read()
                self.setStyleSheet(styleSheet)
        except Exception as e:
            QMessageBox(self, 'Error', 'qss文件读取失败', QMessageBox.Yes)

        # 功能绑定区
        # self.qcbAutoRead.stateChanged.connect(self.checkBoxChanged)
        # self.qcbAutoCopy.stateChanged.connect(self.checkBoxChanged)
        # self.btnExit.clicked.connect(QCoreApplication.exit)
        self.timer.timeout.connect(self.translate)
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

    # checkBox function

    # def checkBoxChanged(self, state):
    #     if self.sender() == self.qcbAutoRead:
    #         self.autoRead = True if(state == 2) else False
    #     elif self.sender() == self.qcbAutoCopy:
    #         self.autoWrite = True if (state == 2) else False

    # fetch the text from textOrigin
    def fetchPlainText(self):
        return self.qteInputText.toPlainText()

    # set the text to textTranslate
    def setPlainText(self, text):
        self.qteResultText.clear()
        self.qteResultText.setPlainText(text)
        return text

    def translate(self):
        if self.autoRead is True:
            text = self.readClipboard()
            if text is None or text == self.res:
                return
            self.qteInputText.clear()
            self.qteInputText.setPlainText(text)
        else:
            text = self.fetchPlainText()
        if text == self.text:
            return
        else:
            self.text = text
        if text is None:
            self.setPlainText('[empty]')
            return
        elif text == self.res:
            return
        if text is not '':
            self.res = self.setPlainText(translate.translate(text))
        self.setPlainText(self.res)
        if self.autoWrite is True:
            self.writeClipboard(self.res)

    def readClipboard(self):
        return translate.gettext()

    def writeClipboard(self, text):
        translate.settext(text)


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
        self.activated.connect(self.iconClied)
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

    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.uiHandle
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()
        # print(reason)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainUX = MainUX()
    sys.exit(app.exec_())
