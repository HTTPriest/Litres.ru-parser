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

        for i in range(1, 2):
            link = 'https://www.litres.ru/legkoe-chtenie/page-%i/' % i
            yield SplashRequest(link,
                                callback=self.parse,
                                args={'wait': 2,
                                      'html': 1,
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

    def seq(self, sequence, path):
        tags = []
        for s in sequence.xpath(path):
            s = s.xpath('string(.)').extract()[0]
            tags.append(s)
        return tags


    def parse_item(self, response):
        prefix = randint(0, 999)

        with open('save/%soutput.png' % prefix, 'wb') as f:
            f.write(b64decode(response.data['png']))
        with open('save/%soutput.html' % prefix, 'w') as f:
            f.write(response.data['html'])

        tags = response.xpath('//li[@class="tags_list"]')
        genres = response.xpath('//div[@class="biblio_book_info"]/ul/li[2]')
        desc = [response.xpath('string(//div[@class="biblio_book_descr_publishers"])').extract(),
                response.xpath('string(//div[@itempror="description"])').extract(),
                response.xpath('string(//div[@class="biblio_book_descr_publishers hide"])').extract()]

        book = LitresItem()
        book['btype'] = response.xpath('//div[@class="biblio_book_type"]/text()').extract()[0]
        book['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()
        book['author'] = response.xpath('//div[@class="biblio_book_author"]/a[@class="biblio_book_author__link"]/text()').extract()
        book['rating'] = response.xpath('//div[@itemprop="aggregateRating"]//span[@class="show_mid_vote"]/text()').extract()
        book['tags'] = self.seq(tags, './a')
        book['genres'] = self.seq(genres, './a')
        book['price'] = response.xpath('//div[@id="unr_buynow"]//span[@class="simple-price"]/text()').extract()
        book['description'] = [descr[0].replace(u'\xa0', ' ') for descr in desc if descr[0] is not '']
        book['ISBN'] = response.xpath('//span[@itemprop="isbn"]/text()').extract()
        #self.log(book)
        yield book

