# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from litres.items import LitresItem
from base64 import b64decode
from random import randint


class LitSpider(scrapy.Spider):
    name = 'lit'
    allowed_domains = ['litres.ru']
    start_urls = ['http://litres.ru/']


    def start_requests(self):
        yield SplashRequest('https://www.litres.ru/legkoe-chtenie/',
                            callback=self.parse,
                            args={'wait': 2,
                                  'html': 1,
                                  'png': 1,
                                  },
                            endpoint='render.json')

    def parse(self, response):
        items = response.xpath('//div[@class="books_box"]//div[@class="art-item__name"]')
        #self.log(items)

        for item in items:
            link = item.xpath('.//a/@href').extract()
            print(link)
            url = 'http://litres.ru/' + link[0]
            yield SplashRequest(url, callback=self.parse_item,
                                args={'wait': 1,
                                      'html': 1,
                                      'png': 1,
                                      },
                                endpoint='render.json')

    def parse_item(self, response):
        prefix = randint(0, 999)

        with open('save/%soutput.png' % prefix, 'wb') as f:
            f.write(b64decode(response.data['png']))
        with open('save/%soutput.html' % prefix, 'w') as f:
            f.write(response.data['html'])

        book = LitresItem()
        book['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()
        book['author'] = response.xpath('//div[@class="biblio_book_author"]/a[@class="biblio_book_author__link"]/text()').extract()
        book['rating'] = response.xpath('//div[@itemprop="aggregateRating"]//span[@class="show_mid_vote"]/text()').extract()
        book['genres'] = response.xpath('//div[@class="biblio_book_info"]//li[2]/a/text()').extract()
        book['tags'] = []
        for tag in response.xpath('//div[@class="biblio_book_info"]//li[@class="tags_list"]'):
            tagr = tag.xpath('.//a/span[@class="uppercase"]/text()').extract()[0] + tag.xpath('.//a/text()').extract()[0]
            self.log('YOYOOYo')
            self.log(tagr)
            print(type(tagr))
            book['tags'] = tagr
        book['price'] = response.xpath('//div[@id="unr_buynow"]//span[@class="simple-price"]/text()').extract()
        book['description'] = response.xpath('//div[@class="biblio_book_descr_publishers"]/p/text()').extract()
        book['ISBN'] = response.xpath('//span[@itemprop="isbn"]/text()').extract()
        self.log(book)
        yield book

