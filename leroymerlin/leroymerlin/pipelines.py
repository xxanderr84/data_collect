# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from lxml import html


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.tools

    def collect_characters(self, item):
        res = {}
        for i in item['characters']:
            dom = html.fromstring(i)
            char_ = dom.xpath('//dt/text()')[0].strip()
            val_ = dom.xpath('//dd/text()')[0].strip()
            res[char_] = val_
        return res

    def process_item(self, item, spider):
        item['characters'] = self.collect_characters(item)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)


class LeroyMerlinPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta={'image_path': item['_id'],
                                                    'image_name': img[img.rfind('/', 0)+1:]})
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        return f"{request.meta['image_path']}\{request.meta['image_name']}"
