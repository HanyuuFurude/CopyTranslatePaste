import win32clipboard as w
import win32con
import requests
import json
import sys
import chardet
import logging
import time
import os
# debug() 调试级别，一般用于记录程序运行的详细信息
# info() 事件级别，一般用于记录程序的运行过程
# warnning() 警告级别，，一般用于记录程序出现潜在错误的情形
# error() 错误级别，一般用于记录程序出现错误，但不影响整体运行
# critical 严重错误级别 ， 出现该错误已经影响到整体运行

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(filename)s \n [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y/%b/%d %H:%M:%S',
    filename='log.log',
    filemode='a'
)
# 翻译

def word(res):
    resList = []
    for ret in json.loads(res["result"])["content"][0]["mean"][0]["cont"]:
        resList.append(ret)
    res = ""
    for i in resList:
        res+=i+'\n'
    return res
def sentence(res):
    resList = []
    for ret in res["data"]:
        resList.append(ret["dst"])
    res = ""
    for i in resList:
        res+=i+'\n'
    return res
# 翻译
def translate(queryString: str):
    head = \
        {
            # "Host": "fanyi.baidu.com",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            # "Accept": "*/*",
            # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Referer": "https://fanyi.baidu.com/",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "X-Requested-With": "XMLHttpRequest",
            # "Connection": "keep-alive"
            "Host":" fanyi.baidu.com",
            "User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
            "Accept":" */*",
            "Accept-Language":" zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding":" gzip, deflate, br",
            "Referer":" https://fanyi.baidu.com/",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With":" XMLHttpRequest",
            "Content-Length":" 121",
            "Connection":" keep-alive",
            "Cookie":" BAIDUID=C06A41C141B090CBD743BAD41E49F8DA:FG=1; BIDUPSID=C06A41C141B090CBD743BAD41E49F8DA; PSTM=1552839539; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1558795642,1558945603,1560824308; from_lang_often=%5B%7B%22value%22%3A%22dan%22%2C%22text%22%3A%22%u4E39%u9EA6%u8BED%22%7D%2C%7B%22value%22%3A%22hu%22%2C%22text%22%3A%22%u5308%u7259%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; pgv_pvi=9974821888; locale=zh; pgv_si=s7580348416; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1560824308; ZD_ENTRY=bing; delPer=0; PSINO=1; H_PS_PSSID=26525_1466_21097_29064_28519_29098_28836_28584; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; yjs_js_security_passport=29d167a6439954367998f3579714aa0d6aa162be_1560824307_js",
            "TE":" Trailers",
        }
    form = {
        "from": "en",
        "to": "zh",
        "query": queryString,
        "source": "txt",
        "simple_means_flag":3,
        "sign":1721.439192,
        "token":"8adacf46fbcb4329dc03d0b85e2cbaab"
    }
    try:
        res = requests.post("https://fanyi.baidu.com/v2transapi", form,headers = head)
        resjson = res.json()
        a={1:'a',2:'b'}
        resFilter={1:word,2:sentence}
        return resFilter[(resjson["type"])](resjson)
    except Exception as e:
        print(e)
        logging.error('[error] network error.')
        return None



# 从剪切板获取文本


def gettext()->str:
    try:
        w.OpenClipboard()
        t = w.GetClipboardData()
        w.CloseClipboard()
        logging.debug('[read from clipboard]:%s' % t)
        return t
    except Exception as e:
        logging.error(str('can\'t read from clipboard.\n %s' % e))
        w.CloseClipboard()
        return None


def settext(aString)->None:
    if aString is not None:
        try:
            w.OpenClipboard()
            # w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
            w.CloseClipboard()
        except Exception as e:
            logging.error('write to clipboard failure %s' % e)
            return None
        finally:
            try:
                w.CloseClipboard()
            except Exception as e:
                logging.critical('close clipboard failure %s' % e)


if __name__ == "__main__":
    pass
    # res = translate('today')
    # for i in res:
    #     print('->'+i)
    # argv = sys.argv
    # s = ''
    # for i in range(1, len(argv)):
    #     # print(i)
    #     s = s + argv[i] + ' '
    # # todo:
    # # add stay at background mode
    # if s == '-b' or s == '--background':
    #     last = ''
    #     while True:
    #         try:
    #             queryWord = gettext()
    #             if last == queryWord:
    #                 res = translate(queryWord)
    #                 settext(res)
    #                 print('[res]:', res)
    #             time.sleep(0.1)  # prevent too much query in short time
    #         except Exception as e:
    #             print(e)
    # else:
    #     res = translate(s)
    #     print('[翻译结果]===================')
    #     print(res)
    #     # res = res.encode('gbk')
    #     settext(res)
    #     print('[已复制到剪切板]===================')
