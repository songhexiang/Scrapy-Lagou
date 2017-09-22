# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from tutorial.items import TutorialItem
import re
import time
import io
import os
import json
  
class LagouSpider(CrawlSpider):  
    name = "lagou"  
    #allowed_domains = ["www.lagou.com"]  
    start_urls = [  
        "https://www.lagou.com/", 
    ]

    headers = {
        'Host': 'passport.lagou.com',
        'Referer': 'https://passport.lagou.com/login/login.html/',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        # 'X-Anit-Forge-Token' : '35ed481a-e85c-45db-bf65-256546725c1c',
        #'X-Anit-Forge-Token': '636a61a6-885a-42f5-8031-bfc3c9c45073',
        # 'X-Anit-Forge-Code' : '99573313',
        #'X-Anit-Forge-Code': '99573313',
        'X-Requested-With': 'XMLHttpRequest'
    }

    request_headers = {
        'Host': 'www.lagou.com',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        # 'X-Anit-Forge-Token' : '35ed481a-e85c-45db-bf65-256546725c1c',
        #'X-Anit-Forge-Token': '636a61a6-885a-42f5-8031-bfc3c9c45073',
        # 'X-Anit-Forge-Code' : '99573313',
        #'X-Anit-Forge-Code': '99573313',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # 重写爬虫类的方法，定义了自定义请求
    def start_requests(self):
        return [Request("https://passport.lagou.com/", 
                        meta={'cookiejar' : 1}, 
                        headers=self.headers, 
                        dont_filter=True, 
                        callback=self.post_login)]
    
    def post_login(self, response):
        print('准备登陆拉勾网......\n')
        #headers添加token项
        data = response.xpath('//script[@type = "text/javascript"]/text()').extract()[1]
        anti_token = {'X-Anit-Forge-Token' : 'None', 'X-Anit-Forge-Code' : '0'}
        anti_token['X-Anit-Forge-Token'], anti_token['X-Anit-Forge-Code'] = re.findall(r'[a-z0-9-]{36}',data)[0],re.findall(r'[0-9]{8}',data)[0]
        login_headers = self.headers.copy()
        login_headers.update(anti_token)
        print(login_headers)
        #头信息添加tokena
        return [FormRequest(url="https://passport.lagou.com/login/login.json",
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            #此处待修改，应当加入token
                            headers = login_headers,  #注意此处的headers是添加了token之后的headers
                            formdata = {
                            'isValidate' : 'true',
                            #此处待更改，拉勾网采用了双重md5加密算法
                            'password' : '8e65949be8bdd54dc895bf9bad5f47a5',
                            'request_form_verifyCode' : '',
                            'submit' : '',
                            'username' : '15929939451'
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]

    def after_login(self, response):
        for i in range(30):
            url = self.start_urls[0]+ "zhaopin/Python/" + str(i+1)+"/"
            yield Request(url, 
                          meta={'cookiejar' : 1}, 
                          headers=self.request_headers,  
                          callback=self.parse_page)
  
    def parse_page(self, response):
        count = len(response.xpath('//a[@class = "position_link"]/h3/text()').extract())
        for i in range(count):
            item = TutorialItem()
            item['position'] = response.xpath('//a[@class = "position_link"]/h3/text()').extract()[i]
            item['money'] = response.xpath('//span[@class = "money"]/text()').extract()[i]
            item['industry'] = response.xpath('//div[@class = "industry"]/text()').extract()[i].strip(' \n')
            item['href'] = response.xpath('//a[@class = "position_link"]/@href').extract()[i]
            yield item
        '''
        # 以下部分是将爬取到的数据写入json文件中
        with io.open('lagou.json', 'w', encoding='utf8') as json_file:
            for i in item:
                json.dump(i, json_file, ensure_ascii=False)
            json.dump(item['position'], json_file, ensure_ascii=False)

        # 以下部分是将采集的url提取当中的关键数字信息
        for site in sites:
            print(site)
            print(re.findall(r"\d{7}",site))
            lst.append(site)
        # 循环爬取页面
        for i in range(2,6):
            url = self.start_urls[0]+str(i)+"/"
            yield scrapy.Request(url, callback=self.parse)
        '''  
