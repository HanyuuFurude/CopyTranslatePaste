# -*- coding: utf-8 -*-
import platform
from utils.clipboardUtils import clipboardWindows
from utils.clipboardUtils import clipboardMacOS

# @ Author    : HanyuuLu
# @ Date      : 2020/08/14
# @ Desc      : Clipboard set get module for Windows and MacOS

ClipboardDict = {
    "Windows": clipboardWindows.ClipboardWindows,
    "Darwin": clipboardMacOS.MacClipboard
}


def clipboardBuilder(OSString: str):
    ClipboardImpl = ClipboardDict[OSString]

    class Clipboard(ClipboardImpl):
        '''
            system specified clipboard class
        '''

        def __init__(self):
            super().__init__()
            pass

        def getSys(self):
            return self.name

        def getText(self):
            '''
                get a text value from top of the stack of clipboard
            '''
            return super().getText()

        def setText(self, text):
            '''
                push a text value to top of the stack of clipboard
            '''
            super().setText(text)

    return Clipboard


clipboard = clipboardBuilder(platform.system())()
