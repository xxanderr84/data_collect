from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from home_work.lesson_06.jobparser import settings
from home_work.lesson_06.jobparser.spiders.LabirintRu import LabirintSpider
from home_work.lesson_06.jobparser.spiders.book24 import Book24Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider)
    process.crawl(Book24Spider)
    process.start()
