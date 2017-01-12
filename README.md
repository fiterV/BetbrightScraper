<h3> Parser for betbright(horse racing site) </h3>

It parses all the <b>international</b> horse races, but not the ones which are in UK and Ireland

To get the information in JSON you need to run:
```
scrapy crawl betty -o result.json -t json
```

To get the information in CSV:
```
scrapy crawl betty -o result.csv -t csv
```
