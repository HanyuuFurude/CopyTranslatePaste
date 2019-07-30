# -*- coding:utf-8 -*-
'''
Created on 2016年12月14日

@author: DXL

Copyright (C) 2004-2019 Shandong Zhaoyuan Software Development Co.,Ltd

'''
import cgitb
cgitb.enable( format='text')
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
import sip
from ctypes.wintypes import *

print (help(MSG))
PADDING = 2
UP,DOWN,LEFT,RIGHT,LEFTTOP,LEFTBOTTOM,RIGHTTOP,RIGHTBOTTOM,UNDIRECT = range(9)
HTLEFT = 10
HTRIGHT = 11
HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOM = 15
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17
HTCAPTION = 2

class CustomWidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def isInTitle(self, xPos, yPos):
        return yPos < 30

    def GET_X_LPARAM(self, param):
        return param & 0xffff

    def GET_Y_LPARAM(self, param):
        return param >> 16

    def nativeEvent(self,eventType,message):
        result = 0
        msg2 = ctypes.wintypes.MSG.from_address(message.__int__())
        minV,maxV = 18,22
        if msg2.message == 0x0084:
            print(msg2)
            xPos = self.GET_X_LPARAM(msg2.lParam) - self.frameGeometry().x()
            yPos = self.GET_Y_LPARAM(msg2.lParam) - self.frameGeometry().y()
#             if self.childAt(xPos,yPos) == 0:
#                 result = HTCAPTION
#             else:
#                 return (False,result)
            if(xPos > minV and xPos < maxV):
                result = HTLEFT
            elif(xPos > (self.width() - maxV) and xPos < (self.width() - minV)):
                result = HTRIGHT
            elif(yPos > minV and yPos < maxV):
                result = HTTOP
            elif(yPos > (self.height() - maxV) and yPos < (self.height() - minV)):
                result = HTBOTTOM
            elif(xPos > minV and xPos < maxV and yPos > minV and yPos < maxV):
                result = HTTOPLEFT
            elif(xPos > (self.width() - maxV) and xPos < (self.width() - minV) and yPos > minV and yPos < maxV):
                result = HTTOPRIGHT
            elif(xPos > minV and xPos < maxV and yPos > (self.height() - maxV) and yPos < (self.height() - minV)):
                result = HTBOTTOMLEFT
            elif(xPos > (self.width() - maxV) and xPos < (self.width() - minV) and yPos > (self.height() - maxV) and yPos < (self.height() - minV)):
                result = HTBOTTOMRIGHT
            else:
                result = HTCAPTION
            return (True,result)
        ret= QWidget.nativeEvent(self,eventType,message)
        return ret





if __name__ == '__main__':
    app = QApplication([])
    try:
        w = CustomWidget ()
        w.show()
    except:
        import traceback
        traceback.print_exc()

    app.exec_()
