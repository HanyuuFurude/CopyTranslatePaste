# -*- coding: utf-8 -*-


class ClipboardWindows:

    # @ Author    : HanyuuLu
    # @ Date      : 2020/08/14
    # @ Desc      : Clipboard getter setter for Windows

    def __init__(self):
        self.name: str = "Windows"
        import win32clipboard as w
        import win32con
        self.w = w

    def getText(self) -> str:
        try:
            self.w.OpenClipboard()
            t = self.w.GetClipboardData()
            return t
        except Exception as e:
            return None
        finally:
            self.w.CloseClipboard()

    def setText(self, text: str) -> None:
        if text is not None:
            try:
                self.w.OpenClipboard()
                self.w.EmptyClipboard()
                self.w.SetClipboardData(win32con.CF_UNICODETEXT, text)
            except Exception as e:
                return None
            finally:
                self.w.CloseClipboard()
