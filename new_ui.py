import sys
# from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow,QPushButton,QStatusBar,QApplication,QMessageBox,QTextBrowser
from PyQt5.QtCore import Qt
import threading
import time
import datetime
class  MainUX(QMainWindow):
	def __init__(self, parent=None, flags=Qt.WindowFlags()):
		super().__init__(parent=parent, flags=flags)
		self.show()
		return 
if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainUX=MainUX()
	sys.exit(app.exec_())