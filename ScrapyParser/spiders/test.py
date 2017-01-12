import scrapy
from cssselect.parser import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import logging
import re
from ScrapyParser.items import ScrapyparserItem
from termcolor import colored
from selenium import webdriver
from bs4 import BeautifulSoup

#Fix the way you find the numbers array for competitors
#because it's made in different ways on FRONT END PAGE ON THE SITE




class MySpider(BaseSpider):
    name='betty'
    allowed_domains = ['betbright.com']
    start_urls = ['https://www.betbright.com/horse-racing/today']

    #combination of XPath and Beautiful soup makes life easier
    def parse_race(self, response):

        sel = Selector(response)
        racecards = (sel.xpath('//ul[@data-disable-event-container="#racecard_"]').extract())

        #easy trick(but slow) that let us avoid the recursion in our algorithm
        if len(racecards)>1:
            for i in range(0, len(racecards)-1):
                racecards[i] = racecards[i].replace(racecards[i+1], '')
        for race in racecards:
            soup = BeautifulSoup(race)
            nameAndTime = soup.find('div', {'class':'event-name'}).getText()
            bufferForGettingNameAndTimeSeparated = nameAndTime.split(' ')
            time, trackName = bufferForGettingNameAndTimeSeparated[0], ' '.join(bufferForGettingNameAndTimeSeparated[1:])
            id = soup.find('ul')['data-event-id']

            horsesParentSoup = soup.find('ul', {'class':'horses-list'})
            participantNames = [c.getText() for c in horsesParentSoup.findChildren('div', {'class': 'horse-information-name'})]
            numbers = [c.getText() for c in horsesParentSoup.findChildren('div', {'class': 'cloth-number'})]
            odds = [c['id'][14:] for c in horsesParentSoup.findChildren('li', {'id': re.compile(r'previous_odds_[\d]+')})]


            participants = list(zip(participantNames, numbers, odds))
            participants = list(set(participants))
            participants = sorted(participants, key=lambda x: int(x[1]))

            item = ScrapyparserItem()
            item['time']=time
            item['trackName'] = trackName
            item['id'] = id
            item['participants']=participants
            item['countOfParticipants'] = len(participants)
            yield item

    def parse(self, response):
        sel = Selector(response)
        items = []

        x = sel.xpath('//table[@class="racing"]/tr/td/a[@class!="event_time "]/@href')
        for i in x:
            href = i.extract()
            if 'international' in href:
                yield scrapy.Request(href, callback=self.parse_race)


        # x = sel.xpath('//table[@class="racing"]/tr/td/a[@class!="event_time "]/text()')
        # for s in x:
        #     item = ScrapyparserItem()
        #     item['name']=s.extract()
        #     print(item)
        #     items.append(item)
        # #print('Answer goes right here')
        # #print(x)
        # return items