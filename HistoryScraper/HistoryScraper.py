

import scrapy
import ujson
import re
import sys
from datetime import datetime
class HistorySpider(scrapy.Spider):
	name = 'historyspider'
	# custom_settings = {
	# 	'DEFAULT_REQUEST_HEADERS': {
	# 		'Authorization': '',
	# 		'X-Developer-Key': ''
	# 	}
	# }
	count = 0
	state = {}
	def __init__(self, auth_token, dev_key, stop_at):
		super(HistorySpider, self)
		self.auth_token = auth_token
		self.dev_key = dev_key
		self.stop_at = int(stop_at)
	def start_requests(self):
		t = (datetime.now() - datetime.utcfromtimestamp(0)).total_seconds()*1000000
		yield scrapy.Request("https://history.google.com/history/api/lookup?client=chrome&titles=1&max=%i&num=150" % t, callback=self.parse, headers = {
			'Authorization': self.auth_token,
			'X-Developer-Key': self.dev_key
		})
	def parse(self, response):
		print ('Count: %i' %  self.state.get('items_count', 0))
		if self.state.get('items_count', 0) > self.stop_at:
			sys.exit(0)
		body = response.body_as_unicode()
		data = ujson.loads(body)
		for ele in data['event']:
			self.state['items_count'] = self.state.get('items_count', 0) + 1
			print ("Scraped url %s" % ele['result'][0]['url'])
			yield self.convert_json_data(ele)
		next_time = (self.convert_json_data(data['event'][-1])['timestamp'] - datetime.utcfromtimestamp(0)).total_seconds()*1000000
		yield scrapy.Request("https://history.google.com/history/api/lookup?client=chrome&titles=1&max=%i&num=150" % next_time, callback=self.parse, headers = {
			'Authorization': self.auth_token,
			'X-Developer-Key': self.dev_key
		})
	def convert_json_data(self, ele):
		obj = {}
		obj['title'] = ele['result'][0]['title']
		obj['url'] = ele['result'][0]['url']
		obj['timestamp'] = datetime.fromtimestamp(int(ele['result'][0]['id'][0]['timestamp_usec'])/1000000)
		return obj
