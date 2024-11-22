# -*- coding: utf-8 -*-

from datetime import datetime
import scrapy
import pymongo


class AlsabahmongoSpider(scrapy.Spider):
    name = 'alsabahmongo'
    allowed_domains = ['alsabaah.iq']
    start_urls = ['http://alsabaah.iq/lastnews/']
    mongo_uri = 'mongodb://localhost:27017/'
    mongo_db = 'alsabah'
    collection_name = 'news'

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]
        self.collection.create_index([('link', pymongo.ASCENDING)], unique=True)
        self.num_of_pages = 50

    def closed(self, reason):
        self.client.close()

    def parse(self, response):

        links = response.xpath('//a[@class="img-box"]/@href')
        for link in links.getall():
            yield response.follow(link, callback=self.parse_link, meta={'link': link})

        next_page_url = response.xpath('//li[@onclick="nextPage()"]/a/@href').get()
        page_number = int(next_page_url.split('/')[-2]) if next_page_url else 0
        if next_page_url and page_number < self.num_of_pages:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_link(self, response):
        link = response.meta['link']
        title = response.xpath('//span[@id="news-title"]/text()').get()
        img = response.xpath('//img[@id="news-img"]/@src').get()
        img_url = response.urljoin(img)
        date_str = response.xpath('//span[contains(@style, "color: var(--main-orange)")]/text()[last()]').get()
        date_object = datetime.strptime(date_str.strip(), '%Y/%m/%d')
        publish_date = int(date_object.timestamp())
        tag = response.xpath('//span[@id="news-category"]/text()').get()
        news_details = response.css('#news-details')
        text = news_details.css('::text').getall()
        text_without_line_breaks = ''.join(text)
        text_with_line_breaks = '\n'.join([t.strip() for t in text if t.strip()])

        news_item = {'link': link, 'title': title, 'publish_date': publish_date, 'img_url': img_url, 'tag': tag,
                     'text_with_line_breaks': text_with_line_breaks,
                     'text_without_line_breaks': text_without_line_breaks}

        try:
            self.collection.update_one({'link': link}, {'$set': news_item}, upsert=True)
        except pymongo.errors.PyMongoError as e:
            self.logger.error('Error while inserting or updating document: %s', e)

        yield news_item
