import json
import requests


def translateYouDao(word: str) -> str:
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'

    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        rawRes = response.text
        res = json.loads(rawRes)['translateResult'][0][0]['tgt']
        return res

    else:
        raise Exception("有道翻译服务不可用")
