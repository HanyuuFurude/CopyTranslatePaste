import win32clipboard as w
import win32con
import requests
import json
import sys
import chardet


def translate(queryString: str)->str:
    form = {
        "from": "en",
        "to": "zh",
        "query": queryString,
        "source": "txt"
    }
    res = requests.post("https://fanyi.baidu.com/transapi", form)
    try:
        resjson = res.json()
        if resjson["type"] == 2:
            return resjson["data"][0]["dst"]
        else:
            for ret in json.loads(resjson["result"])["content"][0]["mean"][0]["cont"]:
                return ret
    except Exception:
        return None


def gettext():
    try:
        w.OpenClipboard()
        t = w.GetClipboardData(win32con.CF_TEXT)
        w.CloseClipboard()
        t = t.decode('gbk')
        return t
    except Exception as e:
        print(e)
        return None



def settext(aString):
    if aString is not None:
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
        w.CloseClipboard()


if __name__ == "__main__":
    argv = sys.argv
    s = ''
    for i in range(1, len(argv)):
        # print(i)
        s = s + argv[i] + ' '
    res = translate(s)
    print('[翻译结果]===================')
    print(res)
    # res = res.encode('gbk')
    settext(res)
    print('[已复制到剪切板]===================')
