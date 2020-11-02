from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlin.leroymerlin import settings
from leroymerlin.leroymerlin.spiders.leroymerlinru import LeroymerlinruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    q = 'шуруповерт'
    process.crawl(LeroymerlinruSpider,  search=q)
    process.start()
