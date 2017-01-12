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
        racecards = BeautifulSoup(sel.extract())
        racecards = racecards.findAll('ul', {'data-disable-event-container':'#racecard_'})
        for i in range(10):
            print(colored('-----------------------------------------------------------------------------------------------> Look over here, boy', color='red'))


        for race in racecards:
            soup = race
            nameAndTime = soup.find('div', {'class':'event-name'}).getText()
            buff = nameAndTime.split(' ')
            time, trackName = buff[0], ' '.join(buff[1:])
            id = soup['data-event-id']

            numberOfParticipants = int(soup['data-participants-no'])

            participantNames = [c.getText() for c in soup.findChildren('div', {'class' : 'horse-information-name'})]
            numbers = [c.find('div').getText() for c in soup.findChildren('div', {'class': 'jockey-silk-container'})]

            participantNames = participantNames[:numberOfParticipants]
            numbers = numbers[:numberOfParticipants]
            participants = list(zip(participantNames, numbers))
            participants = list(set(participants))

            print(colored('new group', 'green'))

            print("Number of participants = {}".format(numberOfParticipants))
            print('Name = {}; Time = {};'.format(trackName, time))
            print('Id = {};'.format(id))

            print("Participants = {}; Count = {};".format(participants, len(participants)))
            print(len(sel.xpath('//div[@class="cloth-number"]')))
            break
            # item = ScrapyparserItem()
            # item['time']=time
            # item['trackName'] = trackName
            # item['id'] = id
            # item['participants']=participants
            # item['countOfParticipants'] = len(participants)
            # return item




        for i in range(10):
            print(colored(
                    '-----------------------------------------------------------------------------------------------> Look over here, boy',
                    color='red'))

                #print('-----------------------------------------------------------------------------------------------> Look over here, boy')
        #print(x)


    def parse(self, response):
        sel = Selector(response)
        items = []

        x = sel.xpath('//table[@class="racing"]/tr/td/a[@class!="event_time "]/@href')
        for i in x:
            href = i.extract()
            return scrapy.Request(href, callback=self.parse_race)


        # x = sel.xpath('//table[@class="racing"]/tr/td/a[@class!="event_time "]/text()')
        # for s in x:
        #     item = ScrapyparserItem()
        #     item['name']=s.extract()
        #     print(item)
        #     items.append(item)
        # #print('Answer goes right here')
        # #print(x)
        # return items