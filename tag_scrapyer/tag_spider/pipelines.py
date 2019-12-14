#!/bin/user/env python

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#新增将获取的数据插入到es中  
import json
from elasticsearch import Elasticsearch, exceptions, helpers

es = Elasticsearch(hosts="http://172.16.2.56", port=9200, timeout=200)


class BlockSpiderPipeline(object):

   def open_spider(self, spider):

       self.fp = open("data.list", "w" )

   def close_spider(self, spider):

       self.fp.close()

   def process_item(self, item, spider):

    #    self.fp.write(item["address"] + " # " + item["tag"] + " # " + item["link"] + " # " + str(item["verified"]) + "\n")
       self.fp.write(item["address"] + " # " + item["tag"] + " # " + item["link"] +'#'+'\n')
       data = {}
       data["address"] = item["address"]
       data["tag"] = item["tag"]
       data["link"] = item["link"]
       #data["verified"] = item["verified"]

       try:
          back = es.index(index="addtags",doc_type="doc",id=item["address"],body=json.dumps(data))
          print(back)
       except Exception as e:
          pass
       return item
