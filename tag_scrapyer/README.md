# 基于Scrapy的比特币地址爬取

这是一个基于Scrapy的爬虫，用于获取公共比特币地址标签的情况。 

安装框架：

    $ [sudo] pip install Scrapy

学习文档：
```
https://scrapy-chs.readthedocs.io/zh_CN/latest/index.html
https://scrapy.org/
```

打开目录 tag_spider/spiders:

    $ cd tag_spider/spiders

然后启动: 

    $ ./run.sh

run.sh 包含Scracpy运行命令: scrapy crawl tagspider. 

Remarks:

1. 可以在文件tag_spider / settings.py中设置爬网页的管道数。:

       ITEM_PIPELINES = {
           'tag_spider.pipelines.BlockSpiderPipeline': 16,
       }

 16是指线程数，可以根据计算机的功能进行自定义。

2. 可以在文件tag_spider / pipelines.py中设置用于保存从网站抓取的数据的文件：

       class BlockSpiderPipeline(object):

           def open_spider(self, spider):

               self.fp = open("data.list", "w" )

 默认文件是“ data.list”， 如有必要，数据也可以保存在数据库中，例如mysql。 可以通过将底层存储从文件更改为数据库来进行自定义。我这里将它插入到es中

3. 爬取得规则在文件中定义 tag_spider/spiders/tagspider.py



