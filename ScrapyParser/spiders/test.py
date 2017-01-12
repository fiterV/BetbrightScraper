import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ScrapyParser.items import ScrapyparserItem
from bs4 import BeautifulSoup
import re

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

            participants = list(set(zip(participantNames, numbers, odds)))
            participants = sorted(participants, key=lambda x: int(x[1]))

            item = ScrapyparserItem()
            item['time']=time
            item['trackName'] = trackName
            item['id'] = id
            item['participants']=participants
            item['countOfParticipants'] = len(participants)
            item['odds']='SP'
            yield item

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//table[@class="racing"]/tr/td/a[@class!="event_time "]/@href')
        for i in links:
            href = i.extract()
            if 'international' in href:
                yield scrapy.Request(href, callback=self.parse_race)