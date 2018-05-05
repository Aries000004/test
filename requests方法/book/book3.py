import requests,re


def Headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/59.0'
    }
    return headers
def book_molu(self,url,headers):
    zhu_url = 'http://www.quanshuwu.com/'
    res = requests.get(url,headers=headers)
    # print(res.text)
    pat = re.compile(r'<strong><a target="(.*?)" href="(.*?)" class="(.*?)">(.*?)</a></strong>', re.S)
    cens = re.findall(pat, res.text)
    items={}
    for cen in cens:
        book_aurl = cen[1]
        book_name = cen[3]
        book_url = zhu_url + book_aurl
        # print(book_name)
        # print(book_url)
        items = {'book_url':book_url}
    return items["book_url"]
def book_milu_txt(self,url,headers):
    zhu_url = 'http://www.quanshuwu.com/'
    res = requests.get(url, headers=headers)
    # res.encoding='utf-8'
    # print(res.text)
    pat = re.compile(r'<li><a href="(.*?)">(.*?)</a></li>', re.S)
    zhangjies = re.findall(pat, res.text)
    # print(zhangjies)
    items={}
    for zhangjie in zhangjies:
        zhangjie_aurl = zhangjie[0]
        zhangjie_name = zhangjie[1]
        zhangjie_url = zhu_url + zhangjie_aurl
        # print(zhangjie_name)
        # print(zhangjie_url)
        items ={'zhangjie_url':zhangjie_url}
    return items['zhangjie_url']
def txt_text(self,url,headers):
    res = requests.get(url, headers)
    # res.encoding = 'utf-8'
    # print(res.text)
    pat = re.compile(r'<p>(.*?)<div class="prenext">', re.S)
    cens = re.findall(pat, res.text)
    # print(cens)
    items={}
    for cen in cens:
        cen = cen.replace('\u3000\u3000', '')
        cen = cen.replace('</p><p>','')
        cen = cen.replace('</p>\r\n\t','')
        # print(cen)
        items = {'cen':cen}
    return items['cen']
def run():
    for i in range(1, 2):
        url = 'http://www.quanshuwu.com/category/8_1_{}.aspx'.format(str(i))
        head = Headers()
        # print(head)
        mulu = book_molu(url, head)
        # print(mulu)
        txt = book_milu_txt(mulu, head)
        # print(txt)
        text = txt_text(txt, headers=head)
        # print(text)
        return text
if __name__ == '__main__':
    run()

