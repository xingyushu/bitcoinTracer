# A Scrapy-based Web Spider

This is a Scrapy-based Web spider to scrawl useful information from public websites. Currently, included in the package is the case for scrawling the tags of public bitcoin addresses. In the future, more cases will be addeded. 

The web spider depends on Scrapy. On ubuntu, it can be installed as:

    $ [sudo] pip install Scrapy

The web spider is easy to use:

First, go to the directory tag_spider/spiders:

    $ cd tag_spider/spiders

Then, running the spider: 

    $ ./run.sh

Note: The file run.sh includes one command of Scracpy: scrapy crawl tagspider. Just for easy use.

Remarks:

1. The number of pipelines to scrawl the webpages can be set in the file tag_spider/settings.py:

       ITEM_PIPELINES = {
           'tag_spider.pipelines.BlockSpiderPipeline': 16,
       }

   The number 16 refers to the number of threads, which can be customized based on the capability of your machine.

2. The file that used to save the data scrawled from the website can be set in the file tag_spider/pipelines.py:

       class BlockSpiderPipeline(object):

           def open_spider(self, spider):

               self.fp = open("data.list", "w" )

   The default file is "data.list". If necessary, the data can also be saved in a database, such as mysql. 
   This can be customized by change the underlaying storage from file to database.

3. The rules for scrawl are defined in the file tag_spider/spiders/tagspider.py

4. More information of Scrapy can be founded at the official website https://scrapy.org/


