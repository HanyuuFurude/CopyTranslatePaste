# -*- coding: utf-8 -*-
'''
@ Author    : HanyuuLu
@ Date      : 2020/08/14
@ Desc      : Clipboard getter setter for Windows
'''


class ClipboardWindows:
    def __init__(self):
        self.name: str = "Windows"
        import win32clipboard as w
        import win32con

    def getText(self) -> str:
        try:
            w.OpenClipboard()
            t = w.GetClipboardData()
            return t
        except Exception as e:
            return None
        finally:
            w.CloseClipboard()

    def setText(self, text: str) -> None:
        if text is not None:
            try:
                w.OpenClipboard()
                w.EmptyClipboard()
                w.SetClipboardData(win32con.CF_UNICODETEXT, text)
            except Exception as e:
                return None
            finally:
                w.CloseClipboard()
