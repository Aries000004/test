import requests,re,json
from requests.exceptions import RequestException
from multiprocessing import Pool
def get_one_page(url):
    '''获取单页内容'''
    try:
        # 不加headers会被猫眼禁止访问
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                 '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        response = requests.get(url, headers=headers)
        # 若状态码等于200代表成功，返回网页结果
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:  # 否则返回空值
        return None

def get_txt(html):
    '''把抓取到源码分析提取想要的信息'''
    #re.S表示匹配所有的字符包括换行符
    pat = re.compile(r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name">'
                     r'<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)'
                     r'</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    items = re.findall(pat,html)
    # print(items)
    #把每一条信息单个提取出来,生成一个字典
    for item in items:
        yield {
            'top':item[0],
            'img':item[1],
            'name':item[2],
            'star':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'grade':item[5]+item[6]

        }
def write_file(content):
    '''把数据写入本地文件,encoding="utf-8表示写入得失中文格式"
    把字典格式用json.dumps(content,ensure_ascii=False)转换
    注意ensure_ascii=False的使用'''
    with open('top.txt','wb+',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+ '\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    # print(url)
    html = get_one_page(url)
    # print(html)
    #遍历内容
    for item in get_txt(html):
        print(item)
        write_file(item)
if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    # pool =Pool()#使用多进程会导致混乱,最好不使用
    # pool.map(main,[i*10 for i in range(10)])