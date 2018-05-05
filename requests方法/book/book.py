import re,time,requests
from urllib import error
'''
全本书屋抓取小说
'''
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/59.0',
    'Content-Type':'text/css; charset=utf-8'
}
zhu_url = 'http://www.quanshuwu.com/'
for i in range(1,2):
    url = 'http://www.quanshuwu.com/category/8_1_{}.aspx'.format(str(i))
    # print(url)
    res = requests.get(url,headers)
    # print(headers)
    # res.encoding = 'cp1252'
    # print(res.text)
    pat = re.compile(r'<strong><a target="(.*?)" href="(.*?)" class="(.*?)">(.*?)</a></strong>',re.S)
    items = re.findall(pat,res.text)
    # print(items)
    for item in items:
        book_aurl = item[1]
        book_name = item[3]
        book_url = zhu_url+book_aurl
        # print(book_name)
        # print(book_url)
        res = requests.get(book_url,headers)
        # res.encoding='utf-8'
        # print(res.text)
        pat = re.compile(r'<li><a href="(.*?)">(.*?)</a></li>',re.S)
        zhangjies = re.findall(pat,res.text)
        # print(zhangjies)
        for zhangjie in zhangjies:
            zhangjie_aurl = zhangjie[0]
            zhangjie_name = zhangjie[1]
            zhangjie_url = zhu_url+zhangjie_aurl
            print(zhangjie_name)
            # print(zhangjie_url)
            res = requests.get(zhangjie_url,headers)
            # res.encoding = 'utf-8'
            # print(res.text)
            pat = re.compile(r'<p>(.*?)<div class="prenext">',re.S)
            cens = re.findall(pat,res.text)
            # print(cens)
            for cen in cens:
                cen = cen.replace('\u3000\u3000', '')
                cen = cen.replace('</p><p>','')
                cen = cen.replace('</p>\r\n\t','')
                # print(cen)
                with open('book.txt','a',encoding='utf-8')as f:
                    f.write('\n'+zhangjie_name+'\n'+'\n'+cen+'\n')