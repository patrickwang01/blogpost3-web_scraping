import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt10293938/']

    
    def parse(self, response):

        cast_crew = response.css("li.ipc-inline-list__item a").attrib["href"]

        yield scrapy.Request(cast_crew, callback = self.parse_full_credits)

    