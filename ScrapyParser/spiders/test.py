import scrapy
from cssselect.parser import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import logging

from ScrapyParser.items import ScrapyparserItem
from termcolor import colored
from selenium import webdriver
from bs4 import BeautifulSoup

#Fix the way you find the numbers array for competitors
#because it's made in different ways on FRONT END PAGE ON THE SITE




class MySpider(BaseSpider):
    name='bet'
    allowed_domains = ['betbright.com']
    start_urls = ['https://www.betbright.com/horse-racing/today']

    def parse_race(self, response):

        sel = Selector(response)
        #racecards = sel.xpath('//div[@class="inner_container"]/descendant::node()/ul')
        #racecards = sel.xpath('//ul[@data-disable-event-container="#racecard_"]')
        racecards = (sel.xpath('//ul[@data-disable-event-container="#racecard_"]').extract())

        #easy trick(but slow) that let us avoid the recursion in our algorithm
        if len(racecards)>1:
            for i in range(0, len(racecards)-1):
                racecards[i] = racecards[i].replace(racecards[i+1], '')
        for i in range(10):
            print(colored('-----------------------------------------------------------------------------------------------> Look over here, boy', color='red'))


        for race in racecards:
            soup = BeautifulSoup(race)
            nameAndTime = soup.find('div', {'class':'event-name'}).getText()
            buff = nameAndTime.split(' ')
            time, trackName = buff[0], ' '.join(buff[1:])
            id = soup.find('ul')['data-event-id']

            horsesParentSoup = soup.find('ul', {'class':'horses-list'})
            participantNames = [c.getText() for c in horsesParentSoup.findChildren('div', {'class': 'horse-information-name'})]
            numbers = [c.getText() for c in horsesParentSoup.findChildren('div', {'class': 'cloth-number'})]
            participants = list(zip(participantNames, numbers))
            participants = list(set(participants))
            participants = sorted(participants, key=lambda x: int(x[1]))

            item = ScrapyparserItem()
            item['time']=time
            item['trackName'] = trackName
            item['id'] = id
            item['participants']=participants
            item['countOfParticipants'] = len(participants)
            yield item




        for i in range(10):
            print(colored(
                    '-----------------------------------------------------------------------------------------------> Look over here, boy',
                    color='red'))

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