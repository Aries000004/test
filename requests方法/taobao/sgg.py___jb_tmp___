import requests
import re
from multiprocessing import Pool
def get_one_pafe(url):
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
def parse_one_page(infolist,html):
    try:
        pattern = re.compile(r',"price":"(.*?)","trace":',re.S)
        price = re.findall(pattern,html)
        pattern = re.compile(r',"title":"(.*?)","pic_url":',re.S)
        title = re.findall(pattern,html)
        # print(price)
        # print(title)
        for x in range(0,48):
            # print(x)
            pric = price[x]
            titl = title[x]
            # print(pric)
            # print(titl)
            infolist.append([pric,titl])
        # print(infolist)
    except:
        # print('')
        return None

def print_phone_list(infolist):
    tplt = "{:4}\t{:8}\t{:6}"
    # print(tplt.format('序号','价格','名字'))
    count = 0
    for g in infolist:
        count+=1
        # print(tplt.format(count,g[0],g[1]))
    # print('')
def write_file(infolist):
    with open('phone.txt','w',encoding='utf-8') as f:
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
        f.close()
def main(depath):
    kw = '手机'
    # depath = 2
    infolist = []
    star_url = 'https://s.taobao.com/search?q='+kw
    # print(star_url)
    for i in range(depath):
        try:
            url = star_url+'&s='+str(48*i)
            # print(url)
            html = get_one_pafe(url)
            # print(html)
            parse_one_page(infolist,html)
        except:
            continue
    print_phone_list(infolist)
    write_file(infolist)


if __name__ == '__main__':
    GROUP_START = 1
    GROUP_END = 1
    asd = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]
    pool = Pool()
    pool.map(main,asd)
    pool.close()
    pool.join()
