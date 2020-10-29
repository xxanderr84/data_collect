import scrapy
from scrapy.http import HtmlResponse
from home_work.lesson_06.jobparser.items import JobparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/zarubezhnaya-fantastika--2050/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='book__title ']/a/@href").extract()
        next_page = response.xpath("//a[contains(text(),'Далее')]/@href").extract_first()
        for link in links:
            yield response.follow(link, callback=self.parse_book)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response: HtmlResponse):
        link = response.url
        title = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//a[@itemprop='author']/text()").extract()
        price = response.xpath("//b[@itemprop='price']/text()").extract_first()
        discount = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        rate = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()
        yield JobparserItem(link=link, title=title, authors=authors,
                            price=price, discount=discount, rate=rate)


