import subprocess
# -*- coding: utf-8 -*-
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
        self.name: str = "Darwin"

    def getText(self) -> str:
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        return str(data, encoding='UTF8')

    def setText(self, text: str) -> None:
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(bytes(text, 'UTF8'))
        p.stdin.close()
        p.communicate()
