# -*- coding: utf-8 -*-
import subprocess
'''
@ Author    : HanyuuLu
@ Date      : 2020/08/14
@ Desc      : Clipboard getter setter for MacOS
'''


class MacClipboard:
    '''
    Clipboard getter setter for MacOS
    '''

    def __init__(self):
        import pyperclip
        self.name: str = "Darwin"

    def getText(self) -> str:
        return pyperclip.paste()
        pass
    '''
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        return str(data, encoding='UTF8')
'''

    def setText(self, text: str) -> None:
        try:
            print("write "+text)
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            p.stdin.write(bytes(text, 'UTF8'))
            p.stdin.close()
            p.communicate()
        except Exception as e:
            print("===")
        finally:
            p.stdin.close()
            p.communicate()
            print("finish write")
