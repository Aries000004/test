import re,time,requests
from urllib import error

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'
}
zhu_url = 'http://top.17k.com/top/top100/06_vipclick/06_vipclick_cnl_man_top_100_pc.html'

res = requests.get(zhu_url,headers=headers)
# print(res.headers)
# res.encoding = 'utf-8'
print(res.text)
pat = re.compile(r'<td><a href="(.*?)" target="(.*?)">(.*?)</a></td>'
                 r'<a class="(.*?)" href="(.*?)" title="(.*?)" target="(.*?)">(.*?)</a></td>'
                 r'<td><a href="(.*?)" title="(.*?) target="(.*?)">(.*?)</a></td><td>(.*?)</td>'
                 r'<td><a href="(.*?)" title="(.*?)" target="(.*?)">(.*?)</a></td>'
                 r'<td width="(.*?)">(.*?)</td><td>(.*?)</td></tr>',re.S)
items = re.findall(pat,res.text)
print(items)
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
        #进行数据清理
        for cen in cens:
            cen = cen.replace('\u3000\u3000', '')
            cen = cen.replace('</p><p>','')
            cen = cen.replace('</p>\r\n\t','')
