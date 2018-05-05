import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
from json import JSONDecodeError
from conf import *
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError
#连接mongdb数据库，创建项目
client=pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]


def get_one_page(offset,keyword):
    '''
    访问网页获取文本信息，动态加载的网页注意查找网页真正的url
    :param offset: 起始参数没词动态加载20
    :param keyword: 想要获取的东西（街拍图片）
    :return: 文本信息
    '''
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    }
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload':'true',
        'count': '20',
        'cur_tab': 1,
        'from': 'search_tab'
    }
    try:
        #实现网页真正的url
        url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        print('请求失败')
        return None

def parse_one_page(html):
    '''
    解析文本信息，提取单个具体信息的url
    使用json.lods()把文本转换成json格式
    '''
    try:
        data = json.loads(html)
        #判断属性是否存在，返回一个生成器
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass
def get_page_datail(url):
    '''
    使用单个信息的url访问信息页面
    :param url: 单个信息的url
    :return: 文本内容
    '''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
        }
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                return res.text
            return None
        except RequestException:
            print('请求失败',url)
            return None
    except JSONDecodeError:
        pass
def parse_page_datail(html,url):
    '''
    解析单个信息的文本内容，用bs提取内容
    :param html: 单个信息的文本内容
    :param url: 单个信息的url
    :return: 返回内容字典
    '''
    try:
        #使用bs解析
        soup = BeautifulSoup(html,'lxml')
        title = soup.select('title')[0].get_text()
        print(title)
        image_pat = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
        # a = re.findall(image_pat,html.decode())
        # print(a)
        result = re.search(image_pat,html)
        # print(result)
        if result:
            # 注意：这里的Json语句包含转义字符 \ ，不去掉会报错
            result = result.group(1).replace('\\', '')
            # print(result)
            data = json.loads(result)
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')#图片url列表
                images = [item.get('url') for item in sub_images]#遍历获取单个图片url
                for image in images: download_image(image)#循环下载
                return {
                    'title':title,
                    'url':url,
                    'images':images
                }
    except JSONDecodeError:
        pass
def download_image(url):  # 传入的是每张图片的地址
    """ 下载图片注意二进制信息保存"""
    print('正在下载', url)  # 调试信息
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                 '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_image(response.content)  # 保存图片，content返回二进制内容（当保存图片视频时）
        return None
    except RequestException:
        print('请求图片出错', url)
        return None
    except JSONDecodeError:
        pass

def save_image(content):
    """存图片"""
    # 定义文件路径，文件名把图片信息md5加密，保证每个文件名不同。
    file_path = '{0}/{1}.{2}'.format(os.getcwd() +
                                     '\imageas', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):  # 如果文件不存在
        with open(file_path, 'wb') as f:
            f.write(content)

def save_to_mongo(result):
    '''存储到mongdb'''
    if db[MONGO_TITLE].insert(result):
        print('存储到Mongo成功')
        return True
    return False


def main(offset):
    html = get_one_page(offset,KEYWORD)
    # print(html)
    for url in parse_one_page(html):
        # print(url)
        html = get_page_datail(url)
        # print(html)
        if html:
            result = parse_page_datail(html,url)
            if result:save_to_mongo(result)
if __name__ == '__main__':
    #使用多线程，线程池启动很慢
    groups = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]  # 生成一个offset列表
    pool = Pool()  # 声明一个进程池
    pool.map(main, groups)
    pool.close()
    pool.join()