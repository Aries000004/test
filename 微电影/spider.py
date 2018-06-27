'''
抓取MP4下载到本地,优酷的只有一个链接,就跳过不访问优酷.
'''
import requests
import re
import threading#多线程
import time
import os,json
from multiprocessing import Pool#多进程
def get_start_html(url):
    '''获得网页源码,是json格式'''
    headers = {
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    response = requests.get(url,headers=headers).text
    # print(response.text)
    return response

def get_one_url(response):
    '''先将文本转换成json数据,获得每个MP4的id'''
    res = json.loads(response)
    centent = re.compile(r'<li class="clearfix" data-id="(.*?)">',re.S).findall(res['data'])
    return centent
def down_flie(video_mp4_url):
    '''获得MP4的二进制内容'''
    response = requests.get(video_mp4_url).content
    return response

def get_video_url(centent):
    '''把MP4二进制文件保存到本地制作成MP4文件'''
    #网站url
    stat_url = 'https://www.vmovier.com/'
    #遍历取出每一个id
    for id in centent:
        #组成 MP4所在的url
        url = stat_url+str(id)
        #获得单个MP4的源码
        response = get_start_html(url)
        # print(response)
        #从源码中提取MP4的标题,播放地址
        video_url = re.compile(r"<title>(.*?)</title>.*?vid='' src='(.*?)'>",re.S).findall(response)
        # print(video_url)
        #判断video_url是否存在
        if video_url:
            # print(video_url)
            #标题
            video_name = video_url[0][0].replace('_场库','')
            #获得MP4播放地址的源码文本
            response = get_start_html(video_url[0][1])
            # print(response)
            #提取MP4的url来下载
            video_mp4_url = re.compile(r'"https_url":"(.*?)"',re.S).findall(response)
            # print(video_mp4_url[0].replace('\\',''))
            #清洗url中的字符
            video_mp4_url = video_mp4_url[0].replace('\\','')
            #返回的二进制内容
            content_mp4 = down_flie(video_mp4_url)
            #写入地址
            path = './movies/{}.mp4'.format(video_name)

            print(path)
            #判断文件是否存在
            if not os.path.exists(path):
                #写入本地
                with open(path,'wb')as f:
                    f.write(content_mp4)
                    #每写入一个就暂停3秒
                    time.sleep(3)

def main(i):
    #每页只有45项(1,2,3)
    url = 'https://www.vmovier.com/post/getbytab?tab=hot&page=1&pagepart='+str(i)
    response = get_start_html(url)
    centent = get_one_url(response)
    get_video_url(centent)
# def start_threading():
#     '''多线程'''
#     th = threading.Thread(target=main)
#     th.start()
if __name__ == '__main__':
    #开启多进程(3)
    p = Pool(3)
    for i in range(1,4):
        #apply_async异步非阻塞式,apply是阻塞式的
        p.apply_async(main, args=(i,))
    p.close()
    p.join()


