# -*- coding: utf-8 -*-
import scrapy
import re

from hashlib import sha1
from collections import deque


class Node:

    def __init__(self):
        self.parent = None
        self.url = None
        # self.color = 0 # 0: white 1: gray 2:black
        self.distance = 100000
        self.children = []
        self.hashcode = 0


class ZhidaoSpider(scrapy.Spider):
    name = "zhidao"
    allowed_domains = ["zhidao.baidu.com"]
    start_urls = (
        'http://www.zhidao.baidu.com/',
    )

    def start_requests(self):
        self.accessed_urls[self.current_node.hashcode] = 1
        yield scrapy.Request(self.current_node.url, self.parse)


    def __init__(self):
        self.processing_queue = deque()
        self.current_node = Node()
        self.current_node.url = "https://zhidao.baidu.com/list?fr=daohang"
        self.current_node.distance = 0
        h = sha1()
        h.update(self.current_node.url)
        self.current_node.hashcode = h.hexdigest()
        self.accessed_urls = dict()
        self.total_pages = 0


    def parse(self, response):
        elements = response.xpath("//body//*[not(self::script)]/text()")
        if elements:
            for element in elements:
                if element:
                    content = element.extract()
                    if len(content.strip()) < 20:
                        continue
                    item = dict()
                    item['content'] = content.strip()
                    yield item

        children = response.xpath("//a[@href]/@href")
        if children:
            for child in children:
                url = child.extract()
                url = response.urljoin(url)
                if re.search("zhidao\S*list", url):
                    print("caught the url.",  url)
                    c = Node()
                        # hash the parent url
                    try:
                        hash_method = sha1()
                        hash_method.update(url)
                        hashcode = hash_method.hexdigest()
                    except :
                        print("error")
                        continue

                    if hashcode in self.accessed_urls:
                        continue
                    else:
                        self.accessed_urls[hashcode] = 1

                    c.parent = hashcode
                    # c.color = 0
                    c.url = url
                    c.distance = self.current_node.distance + 1
                    self.processing_queue.append(c)

        # self.current_node.color = 2
        try:

            if self.total_pages < 5000:
                new_node = self.processing_queue.popleft()
                self.current_node = new_node
                print("access new url", self.current_node.url)
                if new_node.url:
                    yield scrapy.Request(new_node.url, callback=self.parse)
                self.total_pages += 1
        except IndexError:
            print("out of range.")



