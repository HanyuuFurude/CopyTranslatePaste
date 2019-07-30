import sys
# from PyQt5 import *
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import \
    (
        QWidget,
        QMainWindow,
        QPushButton,
        QStatusBar,
        QApplication,
        QMessageBox,
        QTextBrowser,
        QGraphicsRectItem,
        QCheckBox,
        QTextEdit,
        QLabel,
        QVBoxLayout,
        QGridLayout,
        QMessageBox
    )
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
import threading
import time
import datetime
import translate


class MainUX(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.title = 'Seiji'
        self.wgtCanvas = QWidget()
        self.setCentralWidget(self.wgtCanvas)
        self.autoRead = True
        self.autoWrite = True
        self.res = None  # 翻译结果储存变量
        self.text = None  # 待翻译文本储存变量

        # 控件生成
        self.qlbAutoRead = QLabel("自动读取内存文本")
        self.qcbAutoRead = QCheckBox()
        self.qcbAutoRead.setCheckState(Qt.Checked)
        self.qlbAutoCopy = QLabel("自动将结果写入剪切板")
        self.qcbAutoCopy = QCheckBox()
        self.qcbAutoCopy.setCheckState(Qt.Checked)
        self.qlbInputLabel = QLabel("Input box")
        self.qteInputText = QTextEdit()
        self.qlbResultLabel = QLabel("result")
        self.qteResultText = QTextEdit()
        self.btnExit = QPushButton("退出")
        self.timer = QTimer(self)  # 剪切板访问定时器

        # 控件布局
        # 设置区空间布局
        self.wgtSettingArea = QWidget()
        self.QltSettingLayout = QGridLayout()
        self.QltSettingLayout.addWidget(self.qlbAutoRead, 0, 1)
        self.QltSettingLayout.addWidget(self.qcbAutoRead, 0, 0)
        self.QltSettingLayout.addWidget(self.qlbAutoCopy, 1, 1)
        self.QltSettingLayout.addWidget(self.qcbAutoCopy, 1, 0)
        self.wgtSettingArea.setLayout(self.QltSettingLayout)
        # 主ui控件布局
        self.qltMainLayout = QVBoxLayout()
        self.qltMainLayout.addWidget(self.wgtSettingArea)
        # self.qltMainLayout.addWidget(self.qlbAutoRead)
        # self.qltMainLayout.addWidget(self.qcbAutoRead)
        # self.qltMainLayout.addWidget(self.qlbAutoCopy)
        # self.qltMainLayout.addWidget(self.qcbAutoCopy)
        self.qltMainLayout.addWidget(self.qlbInputLabel)
        self.qltMainLayout.addWidget(self.qteInputText)
        self.qltMainLayout.addWidget(self.qlbResultLabel)
        self.qltMainLayout.addWidget(self.qteResultText)
        self.qltMainLayout.addWidget(self.btnExit)
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
        self.setFixedSize(self.width(),self.height())

        # QSS
        try:
            with open('ui.qss', 'r') as r:
                styleSheet = r.read()
                self.setStyleSheet(styleSheet)
        except Exception as e:
            QMessageBox(self, 'Error', 'qss文件读取失败', QMessageBox.Yes)

        # 功能绑定区
        self.qcbAutoRead.stateChanged.connect(self.checkBoxChanged)
        self.qcbAutoCopy.stateChanged.connect(self.checkBoxChanged)
        self.btnExit.clicked.connect(QCoreApplication.exit)
        self.timer.timeout.connect(self.translate)
        self.timer.start(1000)

        self.show()
        return

    # checkBox function

    def checkBoxChanged(self, state):
        if self.sender() == self.qcbAutoRead:
            self.autoRead = True if(state == 2) else False
        elif self.sender() == self.qcbAutoCopy:
            self.autoWrite = True if (state == 2) else False

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainUX = MainUX()
    sys.exit(app.exec_())
