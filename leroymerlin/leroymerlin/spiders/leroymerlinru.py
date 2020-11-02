import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlin.leroymerlin.items import LeroymerlinItem


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        tools = response.xpath('//product-card/@data-product-url')
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        for tool in tools:
            yield response.follow(tool, callback=self.parse_tool)
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        pass

    def parse_tool(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/source[@itemprop='image' "
                                   "and @media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('characters', "//div[@class='def-list__group']")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('_id', "//div[@class='product-detailed-page']/@data-product-id")
        yield loader.load_item()
