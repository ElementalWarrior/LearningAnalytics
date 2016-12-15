

import scrapy
import re
import csv
import html2text
from unidecode import unidecode
from datetime import datetime
import pdb
class MyItem(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	timestamp = scrapy.Field()
	body = scrapy.Field()

	def __repr__(self):
		return self['url']
class CsvSpider(scrapy.Spider):
	name = 'csvspider'
	custom_settings = {
		'RETRY_ENABLED': False
	}
	state = {}
	def __init__(self, history):
		super(CsvSpider, self).__init__()
		self.history = history
	def start_requests(self):
		with open(self.history, 'r') as f:
			reader = csv.reader(f, delimiter=',', quotechar='"')
			isHeader = True
			i = 0
			cols = None
			for line in reader:
				if len(line) == 0:
					continue
				if isHeader:
					cols = line
					isHeader = False
					continue
				url = line[cols.index('url')]
				timestamp = line[cols.index('timestamp')]
				title = line[cols.index('title')]
				i = i + 1
				print ("Item #%i" % i)
				yield scrapy.Request(url, callback=self.parse, meta={'url': url, 'title': title, 'timestamp': timestamp})

	def parse(self, response):
		title = response.meta['title']
		timestamp = response.meta['timestamp']
		url = response.meta['url']

		decoded_response = scrapy.Selector(text=unidecode(response.body.decode('utf-8' if 'encoding' in dir(response) is None else response.encoding)))
		html = ''
		for s in decoded_response.xpath('//body').extract():
			html = html + s

		html = re.sub(r'<script.*?>.*?</script.*?>', '', html)
		html = re.sub(r'<style.*?>.*?</style.*?>', '', html)
		h = html2text.HTML2Text()
		h.ignore_links = True
		h.ignore_images = True
		t = h.handle(html)
		t = re.sub(r'(http[s]?:)?//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', t)
		item = MyItem()
		item['url'] = url
		item['title'] = title
		item['timestamp'] = timestamp
		item['body'] = t
		yield item
