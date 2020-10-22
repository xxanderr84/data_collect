from lxml import html
import requests
from pymongo import MongoClient


def load_news(url: str, params, database):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/86.0.4240.75 Safari/537.36'}
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)
    news = dom.xpath(params['all_news'])
    to_load = []
    for news_item in news:
        site = params['source_metadata']
        title = news_item.xpath(params['title_metadata'])
        link = news_item.xpath(params['link_metadata'])
        date_time = news_item.xpath(params['date_metadata'])
        item_data = {'site': site,
                     'title': title[0],
                     'link': link[0],
                     'date_time': (date_time[0] if len(date_time) > 0 else None)}
        to_load.append(item_data)
    database.insert_many(to_load)


client = MongoClient('127.0.0.1', 27017)
db = client['news']
mail = db.mail
yandex = db.yandex
lenta = db.lenta
mail_params = {'all_news': "//li[@class='list__item']//span[@class='list__text']",
               'title_metadata': "./a/span/text()",
               'link_metadata': "./a/@href",
               'date_metadata': "./something/text()",
               'source_metadata': "mail.ru"}
yandex_params = {'all_news': "//div[@class='mg-grid__col mg-grid__col_xs_4']",
                 'title_metadata': "./article/a/h2/text()",
                 'link_metadata': "./article/a/@href",
                 'date_metadata': "./article//span[@class='mg-card-source__time']/text()",
                 'source_metadata': "Yandex"}
lenta_params = {'all_news': "//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']",
                'title_metadata': "./a/text()",
                'link_metadata': "./a/@href",
                'date_metadata': "./a/time/@datetime",
                'source_metadata': "lenta.ru"}
load_news('https://lenta.ru/', lenta_params, lenta)
load_news('https://yandex.ru/news/', yandex_params, yandex)
load_news('https://news.mail.ru/', mail_params, mail)
