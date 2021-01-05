# -*- coding: utf-8 -*-
import scrapy
#from scrapy.http import Request
from threading import Lock 
from scrapy_redis.spiders import RedisSpider
from JdSpider.utils.cookie_utils import Cookie_Utils
from JdSpider.utils.common import Common
from JdSpider.items import JdspiderItem,JdSpider2Item,JdSpiderCommentItem
import copy
import redis
import re
import json
import time
import random

# class JingDongSpider(scrapy.Spider):
#     name = 'jing_dong'
#     allowed_domains = ['jd.com']
#     #start_urls = ['http://www.jd.com/']

#     def __init__(self):
#         # 爬取总数
#         self.totalCount = 0
#         self.mutex = Lock()  # 线程锁保证线程安全
#         # 动态cookie
#         self.cookie_utils = Cookie_Utils()
#         # 伪造请求头
#         self.headers = {
#             'Connection': 'keep-alive',
#             'Cache-Control': 'max-age=0',
#             'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
#             'sec-ch-ua-mobile': '?0',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Sec-Fetch-Site': 'same-origin',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-User': '?1',
#             'Sec-Fetch-Dest': 'document',
#             'Referer': 'https://search.jd.com/Search?keyword=%E7%BE%BD%E7%BB%92%E6%9C%8D%20%E7%94%B7&enc=utf-8&pvid=320a433bff454ae58390568068086aa9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#         }

#     def start_requests(self):
#         '''准备开始爬取首页数据
#         :return:
#         '''
#          # 第几页，每页30条信息
#         page = 1  
         
#         # 根据销量排行爬取
#         keyword = '羽绒服 男装'
#         wq = '羽绒服 男装'
#         size = 'exsize_M^'
#         #req_url = 'https://search.jd.com/Search?keyword={}&{}&enc=utf-8&pvid=9165188730344362a26024648396b610'.format(keyword, size)

#         req_url = "https://search.jd.com/search?keyword={}&suggest=2.def.0.base&wq={}&ev={}".format(keyword, wq, size)
#         meta = {"keyword": keyword, "size": size, "page": page}
#         req_headers = copy.deepcopy(self.headers)
#         req_headers["Referer"] = req_url
#         req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
#         print(f"准备爬取[{keyword}]第[1]页req_url=[{req_url}]的列表信息\n")
#         yield scrapy.Request(url=req_url, headers=req_headers, callback=self.pagination_parse, meta=meta,
#                       dont_filter=True)

#     def pagination_parse(self, response):
       
#         keyword = response.meta.get('keyword')
#         size = response.meta.get('size')
#         page = response.meta.get('page')
#         goods_list=response.xpath('//*[@id="J_goodsList"]/ul/li')
         
#         if goods_list:  
#             if(1==page):
#                 totalPage=response.xpath('//*[@id="J_topPage"]/span/i/text()').extract_first()
#             else:
#                 totalPage = response.meta.get('totalPage')
     
#             #log_id = re.findall("log_id:'(.*?)'", response.text)[0]
#             #li_index = li_list[3]
#             curr_page = response.xpath('//*[@id="J_topPage"]/span/b/text()').extract_first()
#             for good in goods_list:

#                 good_title = Common.spider_data_by_xpath(good,'./div/div[@class="p-name p-name-type-2"]/a/em')
#                 good_price = float(good.xpath('./div/div[@class="p-price"]/strong/i/text()').extract_first())

#                 shop_obj = good.xpath('./div/div[@class="p-shop"]/span/a/text()')
#                 if shop_obj:    
#                     shop_name = good.xpath('./div/div[@class="p-shop"]/span/a/text()').extract_first()
#                     shop_url = "https:"+good.xpath('./div/div[@class="p-shop"]/span/a/@href').extract_first()
#                 else:
#                     shop_name = good.xpath('./div/div[@class="p-shop"]/@data-shopid').extract_first()
#                     shop_url = 'https://mall.jd.com/index-{}.html'.format(shop_name)


#                 good_tips = Common.spider_data_by_xpath(good, './div/div[@class="p-icons"]/*')
#                 if not good_tips:
#                     good_tips = '广告'
#                 brand = Common.get_brand_name(shop_name, good_title)

#                 good_color = good.xpath('./div/div[@class="p-scroll"]//li')
#                 all_stytle = {}
#                 #获取所有当前尺寸的款式
#                 for color in good_color:
#                     color_sku = color.xpath('./a/@title').extract_first()
#                     data_sku = color.xpath('./a/img/@data-sku').extract_first()
#                     #other_img = color.xpath('./a/img/@data-lazy-img or @data-lazy-img-slave').extract_first()
#                     good_detail = "https://item.jd.com/{}.html".format(data_sku)
#                     item = JdspiderItem(
#                                 website='京东',
#                                 brand=brand,
#                                 shop_name=shop_name,
#                                 shop_url=shop_url,
#                                 good_sku=data_sku,
#                                 good_title=good_title,
#                                 good_price=good_price,
#                                 good_detail=good_detail,
#                                 good_color=color_sku,
#                                 good_tips=good_tips)

#                     self.add_totalCount(1)
#                     #print(f'爬取[{item["good_sku"]}]的信息成功，第{page}页，目前已爬取共[{self.totalCount}]条数据\n')
#                     yield item

#             s = page*30-4
#             page = page+1
#             #req_url = 'https://search.jd.com/s_new.php?keyword={}&suggest=2.def.0.base&wq={}&ev={}}&page={}}&s={}&scrolling=y&log_id={}&tpl=3_M&isList=0&show_items='.format(keyword, keyword, size, page, s, log_id)
#             req_url = "https://search.jd.com/s_new.php?keyword={}&{}&ev={}&psort=3&page={}&s={}&click=0".format(keyword, keyword, size, page, s)
#             meta = {"keyword":keyword, "size":size, "page":page, "totalPage":totalPage}
#             req_headers = copy.deepcopy(self.headers)
#             req_headers["Referer"] = req_url
#             req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
#             #print(f"准备爬取[{keyword}]第[{page}{curr_page}]页req_url=[{req_url}]的列表信息\n")
#             time.sleep(random.random())  
#             if page != 200:
#                 yield scrapy.Request(url=req_url, headers=req_headers, callback=self.pagination_parse, meta=meta,
#                               dont_filter=True)
#             else:
#                 yield None
#         else:
#             print("parse error")
#             yield None

#     # 统计总数
#     def add_totalCount(self, count):
#         self.mutex.acquire()
#         self.totalCount += count
#         self.mutex.release()






class JingDongSpider2(RedisSpider):
    name = 'computer'
    allowed_domains = ['jd.com']
    #start_urls = ['http://www.jd.com/']
    redis_key = "jd_computer:start_urls"

    def __init__(self):
        # 爬取总数
        self.totalCount = 0
        self.mutex = Lock()  # 线程锁保证线程安全
        # 动态cookie
        self.cookie_utils = Cookie_Utils()
        # 伪造请求头
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://list.jd.com/list.html?cat=670%2C671%2C672&ev=exbrand_%E6%88%B4%E5%B0%94%EF%BC%88DELL%EF%BC%89%5E&cid3=672',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    #redisspider类需要重写这个方法，才能实现redis接受start_url
    def make_request_from_data(self, data):
        
        # 根据销量排行爬取
        data = json.loads(data)
        url = data.get('url')
 
        return self.make_requests_from_url(url)
 
    def make_requests_from_url(self, url):
        '''准备开始爬取首页数据
        :return:
        '''
         # 第几页，每页30条信息
        page = 1  
         
        # 根据销量排行爬取
        keyword = ['惠普（HP）']
        
        #req_url = "https://list.jd.com/list.html?cat=670,671,672&ev=exbrand_{}^&cid3=672".format(keyword[0])
        meta = {"keyword": keyword[0], "page": page}
        req_headers = copy.deepcopy(self.headers)
        req_headers["Referer"] = url
        req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
        print(f"准备爬取[{keyword[0]}]第[1]页req_url=[{url}]的列表信息\n")
        return scrapy.Request(url, headers=req_headers, callback=self.pagination_parse, meta=meta,
                      dont_filter=True)
 
    # def start_requests(self):
    #     '''准备开始爬取首页数据
    #     :return:
    #     '''
    #      # 第几页，每页30条信息
    #     page = 1  
         
    #     # 根据销量排行爬取
    #     keyword = ['联想（Lenovo）']
        
    #     req_url = "https://list.jd.com/list.html?cat=670,671,672&ev=exbrand_{}^&cid3=672".format(keyword[0])
    #     meta = {"keyword": keyword[0], "page": page}
    #     req_headers = copy.deepcopy(self.headers)
    #     req_headers["Referer"] = req_url
    #     req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
    #     print(f"准备爬取[{keyword[0]}]第[1]页req_url=[{req_url}]的列表信息\n")
    #     yield scrapy.Request(url=req_url, headers=req_headers, callback=self.pagination_parse, meta=meta,
    #                   dont_filter=True)

    def pagination_parse(self, response):
        
        keyword = response.meta.get('keyword')
        page = response.meta.get('page')
        goods_list=response.xpath('//*[@id="J_goodsList"]/ul/li')
        total_page = response.xpath('//div[@id="J_topPage"]/span/i/text()').extract_first()
        if goods_list:  
            for good in goods_list:
                good_detail = 'https:' + good.xpath('.//div[@class="p-name p-name-type-3"]/a/@href').extract_first()
                good_title = Common.spider_data_by_xpath(good,'.//div[@class="p-name p-name-type-3"]/a/em')
                good_price = good.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
                sku = good.xpath('./@data-sku').extract_first() 
                meta = {'sku':sku, 'title':good_title, 'price':good_price, 'page':page, 'keyword':keyword, 'total_page':total_page}
                req_headers = copy.deepcopy(self.headers)
                req_headers["Referer"] = response.url
                req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
                 
                yield scrapy.Request(url=good_detail, headers=req_headers, callback=self.pagination_detail, meta=meta,
                    dont_filter=False)




    def pagination_detail(self, response):

        keyword = response.meta.get('keyword')
        sku = response.meta.get('sku')
        page = response.meta.get('page')
        price = response.meta.get('price')
        title = response.meta.get('title')
        total_page = response.meta.get('total_page')
        shop_name = response.xpath('//div[@class="name"]/a/text()').extract_first()
        cpu_ = '处理器：(.*?);'
        memory_ = '内存容量：(.*?);'
        ssd_ = '固态硬盘（SSD）：(.*?);'
        gpu_model_ = '显卡型号：(.*?);'
        gpu_type_ = '显卡类别：(.*?);'
        weight_ = '商品毛重：(.*?);'
        color_ = '颜色：(.*?);'
        computer_type_ = '类型：(.*?);'
        thickness_ = '机身材质：(.*?);'
        series_ = '系列：(.*?);'
        pixel_ = '分辨率：(.*?);'
        screen_hz_ = '屏幕刷新率：(.*?);'
        good_name_ = '商品名称：(.*?);'

        good_list = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').extract()             
        if good_list:
            good_str = ';'.join(good_list) + ';'
            good_name = Common.regex_converter(good_name_, good_str)
            cpu = Common.regex_converter(cpu_, good_str)   
            memory = Common.regex_converter(memory_, good_str)
            ssd = Common.regex_converter(ssd_, good_str)
            gpu_model = Common.regex_converter(gpu_model_, good_str)
            gpu_type = Common.regex_converter(gpu_type_, good_str)
            weight = Common.regex_converter(weight_, good_str)
            color = Common.regex_converter(color_, good_str)
            computer_type = Common.regex_converter(computer_type_, good_str)
            thickness = Common.regex_converter(thickness_, good_str)
            series = Common.regex_converter(series_, good_str)
            pixel = Common.regex_converter(pixel_, good_str)
            screen_hz = Common.regex_converter(screen_hz_, good_str)

            item = JdSpider2Item(sku=sku,
                                brand=keyword,
                                price=price,
                                title=title,
                                shop_name=shop_name,
                                good_name=good_name[0],
                                cpu=cpu[0],
                                memory=memory[0], 
                                ssd=ssd[0], 
                                gpu_model=gpu_model[0],
                                gpu_type=gpu_type[0],
                                weight=weight[0],
                                color=color[0],
                                computer_type=computer_type[0],
                                thickness=thickness[0],
                                series=series[0],
                                pixel=pixel[0],
                                screen_hz=screen_hz[0],
                                sku_url=response.url)
            yield item

            s = page*30+1;
            page = page+1        
            req_url = 'https://list.jd.com/list.html?cat=670%2C671%2C672&ev=exbrand_{}^&page={}&s={}&click=0'.format(keyword, page, s)
            
            meta = {"keyword":keyword, "page":page, 'total_page':total_page}
            req_headers = copy.deepcopy(self.headers)
            req_headers["Referer"] = req_url
            req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
            print(f"准备爬取[{keyword}]第[{page}]页req_url=[{req_url}]的列表信息\n")
            time.sleep(random.random())  
            if page != 60:
                yield scrapy.Request(url=req_url, headers=req_headers, callback=self.pagination_parse, meta=meta,
                              dont_filter=False)
            else:
                yield None


# class JingDongSpiderComment(RedisSpider):

#     name = 'comment'
#     allowed_domains = ['jd.com']
#     #start_urls = ['http://www.jd.com/']
#     redis_key = "jd_comment:start_urls"

#     def __init__(self):
#         # 爬取总数
#         self.totalCount = 0
#         self.mutex = Lock()  # 线程锁保证线程安全
#         # 动态cookie
#         self.cookie_utils = Cookie_Utils()
#         # 伪造请求头
#         self.headers = {
#             'Connection': 'keep-alive',
#             'Cache-Control': 'max-age=0',
#             'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
#             'sec-ch-ua-mobile': '?0',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Sec-Fetch-Site': 'same-origin',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-User': '?1',
#             'Sec-Fetch-Dest': 'document',
#             'Referer': 'https://search.jd.com/Search?keyword=%E7%BE%BD%E7%BB%92%E6%9C%8D%20%E7%94%B7&enc=utf-8&pvid=320a433bff454ae58390568068086aa9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#         }

#         HOST = "192.168.1.103"
#         PORT = 6379

#         #首先获取一个redis连接池  , 注意端口号不能使用字符串的方式
#         redisPool = redis.ConnectionPool(host=HOST, port=PORT)
#         #实例化一个redis实例，通过连接池
#         self.r = redis.Redis(connection_pool=redisPool)  

#     def parse(self, response): 

#         if "CommentsCount" in response.text:
#             res = json.loads(response.text)["CommentsCount"][0]

#             sku = re.findall("(?<==)\d+",response.url)[0]
#             comment = res["CommentCount"]
#             good_comment_rate = res["GoodRate"]
#             bad_comment_rate = res["PoorRate"]
#             item = JdSpiderCommentItem(sku=sku,
#                                         comment=comment,
#                                         good_comment_rate=good_comment_rate,
#                                         bad_comment_rate=bad_comment_rate)
#             yield item
#         else:
#             r.sadd("comment:fail", response.url)
#             yield None