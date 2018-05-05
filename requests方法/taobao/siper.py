'''
爬取淘宝搜索手机首页
抓取手机的基本信息（排行，名称，价格）
数据持久化写入本地文件
序号  	价格      	名字
1	   9981    	    华为 MATE RS保时捷版
'''
import requests
import re
from urllib.parse import urlencode
def get_one_pafe(url):
    '''访问网页获得网页文本信息'''
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                 '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        res = requests.get(url, headers=headers)
        #如果请求出现错误，就跑出异常，检查要访问的网页的编码格式，
        #并转换（不是很精确，有可能会出现错误）
        # res.raise_for_status()
        # res.encoding=res.apparent_encoding
        if res.status_code == 200:
            # print(res.request.headers)
            return res.text
    except:
        return '连接错误'
def parse_one_page(infolist,html):
    '''
    获得网页文本，使用正则提取想要的数据，并保存到一个list里
    :param infolist: 要保存的list
    :param html: 要解析的网页文本
    :return: 返回一个新的list
    '''
    try:
        pattern = re.compile(r',"price":"(.*?)","trace":',re.S)
        price = re.findall(pattern,html)
        pattern = re.compile(r',"title":"(.*?)","pic_url":',re.S)
        title = re.findall(pattern,html)
        for x in range(0,len(title)):
            # print(x)
            pric= price[x]
            titl = title[x]
            infolist.append([pric,titl])
        # print(infolist)
    except:
        # print('')
        return None

def print_phone_list(infolist):
    '''
    把获得的list进行优化，输出在工作台，更方便查看
    :param infolist: 存放内容的list
    :return: None
    '''
    #表头
    tplt = "{:4}\t{:8}\t{:6}"
    print(tplt.format('序号','价格','名字'))
    #添加序号从0开始，每次加1
    count = 0
    #遍历list
    for g in infolist:
        count+=1
        #g[0]表示g列表的第一个元素，g[1]表示g列表的第2个元素
        print(tplt.format(count,g[0],g[1]))
    #增加换行
    print('')
def write_file(infolist):
    '''
    数据持久化写入文件
    :param infolist: 存放内容的list
    :return: None
    '''
    #用with as 打开文件，用’w‘方法创建一个文件，用’a‘在已有的文件上追加内容
    #添加写入格式
    with open('笔记本电脑.txt','w',encoding='utf-8') as f:
        # print(infolist)
        tplt = "{:4}\t{:8}\t{:6}"
        text_head = tplt.format('序号', '价格', '名字')
        # print(text_head)
        f.write(text_head+'\n')
        count = 0
        for g in infolist:
            count += 1
            text = tplt.format(count, g[0], g[1])
            # print(text)
            f.writelines(text+'\n')

def main():
    kw = '笔记本电脑'#搜索的内容
    depath = 1#想要检索的页数
    infolist = []#接受提取信息的list
    star_url = 'https://s.taobao.com/search?q='+kw
    # print(star_url)
    #使用遍历
    for i in range(depath):
        try:
            #观察网页url格式每页后缀是48的倍数
            url = star_url+'&s='+str(48*i)
            # print(url)
            html = get_one_pafe(url)
            # print(html)
            parse_one_page(infolist,html)
        except:
            continue
    # print_phone_list(infolist)
    # write_file(infolist)
    get_url_cen()


if __name__ == '__main__':
    main()