import requests
from urllib.parse import urlencode
import re
import pymongo
client = pymongo.MongoClient('localhost')
#创建项目名称
db = client['Computer']

def get_url_cen():
    item = {}
    start_url='https://s.taobao.com/search?q='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                             '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    data = {
        "spm":"a230r.1.0.0.123e57e1zztCi8",
        "q": "笔记本电脑",
        "spu_title": "苹果+MACBOOK+AIR+(MQD32CH/A)",
        "app": "detailproduct",
        "pspuid": "1520794",
        "cat": "1101",
        "from_pos": "20_1101.default_0_1_1520794",
        "spu_style":"grid",
    }
    data = urlencode(data)

    url = start_url+data
    # print(url)
    res = requests.get(url,headers=headers)
    # print(res.text)
    pat = re.compile(r'"tag_info":\[(.*?)\],"params":\[(.*?)\],"tag"',re.S)
    cen = re.findall(pat,res.text)
    characteristic = cen[0][0].replace('"text":', '').replace('"','')
    parameter = cen[0][1].replace('"name":','').replace('"value":','').replace('"','')
    item['charcteristic'] = characteristic
    item['parameter'] = parameter
    print(item)
    return item

def save_to_mongdb(item):
    if db['articles'].update({'title':item['title']},{'$set':item},True):
        print("存储到mongdb成功",item['title'])
    else:
        print("存储失败",item['title'])


if __name__ == '__main__':
    get_url_cen()
