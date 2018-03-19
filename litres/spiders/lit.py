# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from base64 import b64decode


class LitSpider(scrapy.Spider):
    name = 'lit'
    allowed_domains = ['litres.ru']
    start_urls = ['http://litres.ru/']


    def start_requests(self):
        yield SplashRequest('https://www.litres.ru/legkoe-chtenie/',
                            callback=self.parse,
                            args={'wait': 2,
                                  },
                            endpoint='render.html')


    def parse(self, response):
       # with open('pic.png', 'wb') as f:
        #    f.write(b64decode(response.data['png']))

       # with open('response.html', 'w') as f:
        #    f.write(response.data['html'])

        #resp = response.data['html']

        items = response.html.xpath('//div[@class=contains(., "cover cover")]/@data-obj')
        self.log(items)