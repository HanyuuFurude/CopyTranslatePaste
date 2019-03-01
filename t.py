import win32clipboard as w
import win32con
import requests
import json
import sys
import chardet
import logging

# debug() 调试级别，一般用于记录程序运行的详细信息
# info() 事件级别，一般用于记录程序的运行过程
# warnning() 警告级别，，一般用于记录程序出现潜在错误的情形
# error() 错误级别，一般用于记录程序出现错误，但不影响整体运行
# critical 严重错误级别 ， 出现该错误已经影响到整体运行

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] $(filename)s \n [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y/%b/%d %H:%M:%S',
    filename='log.log',
    filemode='a'
)
# 翻译


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

# 从剪切板获取文本


def gettext()->str:
    try:
        w.OpenClipboard()
        t = w.GetClipboardData(win32con.CF_TEXT)
        w.CloseClipboard()
        t = t.decode('gbk')
        logging.debug(str('[read from clipboard]:', t))
        return t
    except Exception as e:
        logging.error(str('can\'t read from clipboard.\n', e))
        return None


def settext(aString)->None:
    if aString is not None:
        try:
            w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
            w.CloseClipboard()
        except Exception as e:
            logging.error(str('write to clipboard failure', e))
            return None
        finally:
            try:
                w.CloseClipboard()
            except Exception as e:
                logging.critical(str('close clipboard failure', e))


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
