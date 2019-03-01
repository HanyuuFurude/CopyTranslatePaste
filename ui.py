import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QCheckBox, QLabel, QPlainTextEdit, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QCoreApplication, QTimer
import t
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] $(filename)s \n [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y/%b/%d %H:%M:%S',
    filename='log.log',
    filemode='a'
)


class ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = None
        self.text = None
        # code to get and draw ui
        self.autoRead = True
        self.autoWrite = True
        # self=QMainWindow()
        loadUi('mainwindow.ui', self)
        self.checkBoxR = self.findChild(QCheckBox, 'checkBoxR')
        self.checkBoxR.stateChanged.connect(self.checkBoxChanged)
        self.checkBoxW = self.findChild(QCheckBox, 'checkBoxW')
        self.checkBoxW.stateChanged.connect(self.checkBoxChanged)
        self.textRead = self.findChild(QPlainTextEdit, 'textOrigin')
        self.textWrite = self.findChild(QPlainTextEdit, 'textTranslate')
        self.buttonExit = self.findChild(QPushButton, 'buttonExit')
        self.buttonExit.clicked.connect(
            QCoreApplication.exit)  # button on exit
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.translate)  # 计时结束调用operate()方法
        self.timer.start(1000)  # 设置计时间隔并启动
        self.show()

    # checkBox function
    def checkBoxChanged(self, state):
        if self.sender() == self.checkBoxR:
            self.autoRead = True if(state == 2) else False
        elif self.sender() == self.checkBoxW:
            self.autoWrite = True if (state == 2) else False

    # fetch the text from textOrigin
    def fetchPlainText(self):
        return self.textRead.toPlainText()

    # set the text to textTranslate
    def setPlainText(self, text):
        self.textWrite.clear()
        self.textWrite.appendPlainText(text)
        return text

    def translate(self):
        if self.autoRead is True:
            text = self.readClipboard()
            if text is None or text == self.res:
                return
            self.textRead.clear()
            self.textRead.appendPlainText(text)
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
        self.res = self.setPlainText(t.translate(text))
        self.setPlainText(self.res)
        if self.autoWrite is True:
            self.writeClipboard(self.res)

    def readClipboard(self):
        return t.gettext()

    def writeClipboard(self, text):
        t.settext(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = ui()
    sys.exit(app.exec_())
