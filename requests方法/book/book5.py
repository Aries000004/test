import requests,re,time,random,threading
from bs4 import BeautifulSoup
req_header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cookie':'__cfduid=d577ccecf4016421b5e2375c5b446d74c1499765327; UM_distinctid=15d30fac6beb80-0bdcc291c89c17-9383666-13c680-15d30fac6bfa28; CNZZDATA1261736110=1277741675-1499763139-null%7C1499763139; tanwanhf_9821=1; Hm_lvt_5ee23c2731c7127c7ad800272fdd85ba=1499612614,1499672399,1499761334,1499765328; Hm_lpvt_5ee23c2731c7127c7ad800272fdd85ba=1499765328; tanwanpf_9817=1; bdshare_firstime=1499765328088',
'Host':'www.qu.la',
'Proxy-Connection':'keep-alive',
'Referer':'http://www.qu.la/book/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}
zhu_url = 'http://www.quanshuwu.com/book/'
bookid_url = 'http://www.quanshuwu.com'
def book(book_id):
    book_name = {}
    book_name['title'] = ''
    book_url = zhu_url+str(book_id)+'.aspx'
    # print(book_url)
    res = requests.get(book_url,params=req_header,timeout=100)
    soups = BeautifulSoup(res.text,'html.parser')
    book_name['title'] = soups.select('#main #bookinfo .ti h1')[0].text
    # print(book_name['title'])
    pat = re.compile(r'<li><a href="(.*?)">(.*?)</a></li>', re.S)
    zhangjies = re.findall(pat, res.text)
    # print(zhangjies)

    for zhangjie in zhangjies:
        zhangjie_aurl = zhangjie[0]
        zhangjie_name = zhangjie[1]
        zhangjie_url = bookid_url + zhangjie_aurl
        # print(zhangjie_name)
        # print(zhangjie_url)
        res = requests.get(zhangjie_url, params=req_header,timeout=100)
        # res.encoding = 'utf-8'
        # print(res.text)
        pat = re.compile(r'<p>(.*?)<div class="prenext">', re.S)
        cens = re.findall(pat, res.text)
        # print(cens)
        for cen in cens:
            cen = cen.replace('\u3000\u3000', '')
            cen = cen.replace('</p><p>', '')
            cen = cen.replace('</p>\r\n\t', '')
            # print(cen)
            with open('{}.txt'.format(book_name['title']), 'a', encoding='utf-8')as f:
                f.write('\n' + zhangjie_name + '\n' + '\n' + cen + '\n')
                time.sleep(0.001)

# class myThread (threading.Thread):   #继承父类threading.Thread
#     def __init__(self, threadID, counter,start_page):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.counter = counter
#         self.start_page=start_page
#     def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         #print("编号为1的小说")
#         book(self.counter)
#         #print("Exiting")
# threadLock = threading.Lock()
# threads = []

if __name__ == '__main__':
    book(3847)