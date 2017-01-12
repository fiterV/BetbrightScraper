# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
from .settings import CSV_FILE_PATH

def save(item):
    fileHandler = open(CSV_FILE_PATH, 'a')
    writer = csv.writer(fileHandler, lineterminator='\n')
    if os.fstat(fileHandler.fileno()).st_size == 0:
        writer.writerow([ 'raceName', 'raceId', 'participantName', 'participantId', 'clothNumber', 'time', 'odds'])
    writer.writerow([item['raceName'],
                     item['raceId'],
                     item['participantName'],
                     item['participantId'],
                     item['clothNumber'],
                     item['time'],
                     item['odds'], ])
#CORRECT ORDER
# 'raceName', 'raceId', 'participantName', 'participantId', 'clothNumber', 'time', 'odds'
class ScrapyparserPipeline(object):
    def process_item(self, item, spider):
        save(item)
        return item