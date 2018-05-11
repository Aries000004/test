# -*- coding: utf-8 -*-
'''
模拟登陆
适用于输入型验证码
账号密码用的时候再输入
'''

import scrapy
from scrapy import Request,FormRequest

import urllib.request

class DouSpider(scrapy.Spider):
    name = 'dou'
    allowed_domains = ['douban.com']
    # start_urls = ['http://douban.com/']
    #username= ''
    #word = ''
    def start_requests(self):
        #访问登录页面，打开cookiejar收集
        return [Request('https://accounts.douban.com/login',callback=self.parse,meta={'cookiejar':1})]
    def parse(self, response):
        captcha = response.xpath('//img[@id="captcha_image"]/@src').extract()
        print(captcha)
        #判断是否有captcha，有，就会大于0
        if len(captcha)>0:
            print("现在有验证码")
            #验证码下载路径，路径后面要添加图片名字和格式（a.png）
            localpath = 'C:/Users/40423/Desktop/验证码/yzm.png'
            #urllib.request.urlretrieve（图片地址（url），文件名）把图片下载到本地
            urllib.request.urlretrieve(captcha[0],filename=localpath)
            print("请查看本地验证码图片并输出验证码")
            captcha_value = input()
            # name是邮箱账号，word是密码，有验证码可以查看后在控制到输入
            # redir是登录成功后跳转的页面，可以随意修改
            data = {
                "form_email":username,
                "form_password":word,
                "captcha-solution":captcha_value,
                "redir":"https://www.douban.com/people/178219061/",
            }
        else:
            print("现在没有验证码")
            data = {
                "form_email": username,
                "form_password": word,
                "redir": "https://www.douban.com/people/178219061/",
            }
        print("登录中...")
        return [FormRequest.from_response(response,meta={"cookiejar":response.meta["cookiejar"]},
                                          formdata=data,
                                          callback=self.next)]
    def next(self,response):
        '''登陆成功后就可以进行想要解析'''
        print("登陆成功")


