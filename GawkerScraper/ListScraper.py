

import scrapy
from scrapy.shell import inspect_response
from scrapy.crawler import CrawlerProcess
import logging
import pdb
from unidecode import unidecode

# process = CrawlerProcess({
# 	'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

class ListSpider(scrapy.Spider):
	name = 'listspider'
	start_urls = ['http://gizmodo.com/']
	state = {}
	def __init__(self, stop_at):
		super(ListSpider, self).__init__()
		self.stop_at = int(stop_at)
	def parse(self, response):
		post_links = response.css('.post-wrapper')
		if self.state.get('items_count', 0) > self.stop_at:
			sys.exit(0)
		for link in post_links:
			title = link.css('.headline a::text').extract_first()
			href = link.css('.headline a::attr(href)').extract_first()

			# pdb.set_trace()

			if title is None:
				title = ''
			else:
				title = title.strip()
			if href is None:
				href = ''
			else:
				href = href.strip()
			# print '%s %s' % (title, href)
			if href == '' or title == '':
				continue
			yield scrapy.Request(href, callback=self.parse_page)
			self.state['items_count'] = self.state.get('items_count', 0) + 1

		next_page = response.css('.load-more__button > a::attr(href)').extract_first()
		# inspect_response(response, self)
		if next_page is not None:
			yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

	def parse_page(self, response):
		#get text from nested html tags
		text_nodes = response.xpath('//*[contains(@class,"post-content")]//*//text()')
		data = ''
		new = []
		for t in text_nodes.extract():
			#clean up the unicode strings
			new.append(unidecode(t).strip())

		#filter out empty elements
		new = filter(None, new)

		#filter out the Advertisement elements
		def filter_ad(ele):
			if ele == 'Advertisement':
				return False
			else:
				return True
		new = filter(filter_ad, new)

		#create a single string to export.
		for ele in new:
			#there is some weird character being added that breaks csv format.
			ele = ele.replace('\x0a', ' ')
			data += ' ' + ele
		print("Scraped %s" % response.url)
		yield { 'title': response.css('.headline > a::text').extract_first()
				, 'data': data
				, 'post_time': response.css('.meta__time::attr(datetime)').extract_first()
				, 'author': response.css('.author > a::text').extract_first()
				, 'url': response.url}
#
#
# process.crawl(ListSpider)
# process.start()
