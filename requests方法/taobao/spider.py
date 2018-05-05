import requests
from urllib.parse import urlencode
import re
import pymongo
client = pymongo.MongoClient('localhost')
#创建项目名称
db = client['Computer']

def get_one_pafe(url):
    '''获得搜索主页内容'''
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                 '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res.encoding=res.apparent_encoding
        if res.status_code == 200:
            # print(res.request.headers)
            return res.text
    except:
        return '连接错误'
def parse_one_page(item,html):
    '''解析网页获得商品信息，返回一个生成器'''
    try:
        pattern = re.compile(r',"price":"(.*?)","trace":',re.S)
        price = re.findall(pattern,html)
        pattern = re.compile(r',"title":"(.*?)","pic_url":',re.S)
        title = re.findall(pattern,html)
        pattern = re.compile(r',"month_sales":"(.*?)","seller":',re.S)
        month_sales = re.findall(pattern,html)
        pattern = re.compile(r'"vertical_from_pos":\[(.*?)\],"catdirectForMaidian"',re.S)
        shujus = re.findall(pattern,html)
        # print(urls[0])
        # print(type(urls[0]))
        shuju = shujus[0].split(",")
        # print(type(urls))
        for shuju in shuju:
            pspuid = shuju.split('_')[4].replace('"','')
            from_pos = shuju.replace('"','')
            # print(from_pos)
            item['pspuid'] = pspuid#商品的id
            item['from_pos'] = from_pos#商品的代号
            # print(item)
            # prinitem
        for x in range(0,len(title)):
            # print(x)
            item['price']= price[x]#价格
            item['title'] = title[x]#名称
            item['month_sales'] = month_sales[x]#月成交量
            # print(item)
            yield item
        # print(infolist)
    except:
        # print('')
        return None

def get_url_cen(keyword,item):
    '''
    获得
    :param keyword:要搜索的东西
    :param item:存储的字典变量
    :return:返回一个新的字典
    '''
    try:
        start_url='https://s.taobao.com/search?q='
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                 '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        data = {
            "spm":"a230r.1.0.0.123e57e1zztCi8",
            "q": keyword,
            "spu_title": item['title'],
            "app": "detailproduct",
            "pspuid": item['pspuid'],
            "cat": "1101",
            "from_pos": item['from_pos'],
            "spu_style":"grid",
        }
        data = urlencode(data)
        url = start_url+data
        # print(url)
        res = requests.get(url,headers=headers)
        # print(res.text)
        #获得的是一个list【里面是一个大的字符串，需要用replace（）来去掉不必要的东西
        pat = re.compile(r'"tag_info":\[(.*?)\],"params":\[(.*?)\],"tag"',re.S)
        cen = re.findall(pat,res.text)
        characteristic = cen[0][0].replace('"text":', '').replace('"','')
        parameter = cen[0][1].replace('"name":','').replace('"value":','').replace('"','')
        item['charcteristic'] = characteristic
        item['parameter'] = parameter
        # print(item)
        return item
    except IndexError:
        return None
def save_to_mongdb(item):
    #检查title是否有重复，如果有重复就更新，不会再次生成一个新的，没有就追加，固定方法
    if db['articles'].update({'title':item['title']},{'$set':item},True):
        print("存储到mongdb成功",item['title'])
    else:
        print("存储失败",item['title'])

def main():

    kw = '笔记本电脑'#搜索的商品
    depath = 11#想要搜索的页数
    item = {}#接受数据的字典变量
    #搜索商品首页
    star_url = 'https://s.taobao.com/search?q=' + kw
    for i in range(depath):
        try:
            #商品下一页
            url = star_url+'&s='+str(48*i)
            # print(url)
            html = get_one_pafe(url)
            # print(html)
            for data in parse_one_page(item,html):
                # print(data)
                item = get_url_cen(kw,data)
                save_to_mongdb(item)
        except:
            #出现错误跳过
            continue
if __name__ == '__main__':
    main()