# -*- coding: utf-8 -*-
import json
import requests

from utils.web.translateYouDao import translateYouDao
'''
@ Author    : HanyuuLu
@ Date      : 2020/08/14
@ Desc      : Clipboard set get module for Windows and MacOS
'''
translateDict = {
    "YouDao": translateYouDao
}


def translate(text: str, provider: str = 'YouDao') -> str:
    return translateDict[provider](text)
