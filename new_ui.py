import sys
# from PyQt5 import *
from PyQt5.QtWidgets import \
	(
		QMainWindow,
		QPushButton,
		QStatusBar,
		QApplication,
		QMessageBox,
		QTextBrowser,
		QGraphicsRectItem,
		QCheckBox
	)
from PyQt5.QtCore import Qt
import threading
import time
import datetime
class  MainUX(QMainWindow):
	def __init__(self, parent=None, flags=Qt.WindowFlags()):
		super().__init__(parent=parent, flags=flags)
		self.res=None	# 翻译结果储存变量
		self.text=None	# 待翻译文本储存变量
		self.qcbRes = QCheckBox()
		self.qcbText = QCheckBox()
		
		self.show()
		return 
if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainUX=MainUX()
	sys.exit(app.exec_())