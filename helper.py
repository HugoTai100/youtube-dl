from __future__ import unicode_literals
from mutagen.easyid3 import EasyID3
from scrapy.http import Request, Response
import scrapy
from scrapy.crawler import CrawlerProcess
import re

# metatag = EasyID3('*AL6qDCaAMeMgrinpYgihoQ==.mp3')
# metatag['title'] = "Song Title"
# metatag['artist'] = "Song Artist"
# metatag['tracknumber'] = '7/7'
# metatag['discnumber'] = '7/7'
# metatag['date'] = '2018'
# metatag.save()

import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {}
kkk = ''
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = (
            'http://www.joox.com/hk/en/album/fvoidtJMpWSw29CMm3Abtg==',
    )

    def parse(self, response):
        kkk = response.xpath('//li[contains(@class, "album")]//a[contains(@href, "single")]//@href').extract()
        album_title = response.xpath('//span[contains(@itemprop, "name")]/text()').extract_first()
        songCount = response.xpath('//span[contains(@class, "jsx-3264871046 songCount")]/text()').extract_first()
        year = response.xpath('//span[contains(@itemprop, "albumRelease")]/text()').extract_first()
        year = year[-4:]
        counter = 1
        for i in response.xpath('//li[contains(@class, "album")]//a[contains(@href, "single")]'):
            titlee = i.xpath('./@title').extract_first()
            urll = i.xpath('./@href').extract_first()
            print(urll[2:])
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([urll[2:]])
                filenameid = urll.rfind('/')

                metatag = EasyID3(titlee.replace(':', ' -').replace('"', '\'').replace('?', '').replace('/', '_') + '-' + urll[filenameid + 1:] + '.mp3')
                metatag.delete()
                metatag['title'] = titlee
                metatag['artist'] = "鄭融"
                metatag['albumartist'] = "鄭融"
                metatag['album'] = album_title
                metatag['tracknumber'] = str(counter) + '/' + songCount
                counter += 1
                metatag['discnumber'] = '1/1'
                metatag['date'] = year
                metatag.save()

        return {}


process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
print(kkk)
