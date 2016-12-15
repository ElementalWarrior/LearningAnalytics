

import scrapy
import ujson
import re
from datetime import datetime
class HistorySpider(scrapy.Spider):
	name = 'historyspider'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS':{
		"origin": "https://myactivity.google.com"
		# , "accept-encoding": "gzip, deflate, br"
		, "accept-language": "en-GB,en-US;q=0.8,en;q=0.6"
		, "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
		, "content-type": "application/json;charset=UTF-8"
		, "accept": "application/json, text/plain, */*"
		, "referer": "https://myactivity.google.com/item"
		, "authority": "myactivity.google.com"
		, "x-client-data": "CIS2yQEIpLbJAQjEtskBCMKaygEIqZ3KAQ=="}
	}
	def start_requests(self):
		yield scrapy.Request("https://myactivity.google.com/item?jspb=1", body=ujson.dumps({"ct":"AODP23YAAAEFCoICH4sIAAAAAAAAAOMS4GAUmNb5ilXi7ov1V3omXmDiAomcetHNJrHp392WfpAIPweTwIRFIRJX9095-2oCWAkzRNPNCw1_3vSDRdggIns-7nvfCVFTI3Ds01UpicNNky5NARkjyNHIKPDy2ytZiePrv-1phQg1MQr8nvMaRWgSo8DpiZ_kJP5vPrbvTD9YaAajwPR_p-UlPrx9PrMPomo31JWTH__aP38SWOgQo8CvK7dEJWbcOtfQD1F1Fqjx9hQVieal7_Zth5i1mEng1vsV-hJn3666PQui8RyTQMeyU3wSB-_N_jQXKCQwE2qCFBeHhACjBLtC00kVAOF3Jp8rAQAArg50IeSjGS3sTli8CA5UbADNA4w"}), method="POST", cookies=cooks, callback=self.parse, dont_filter=True)
	def parse(self, response):
		body = response.body_as_unicode()[6:]
		old_body = None
		while old_body is None or old_body != body:
			old_body = body
			body = re.sub(r',,', r',"",', body, 1)
		print (body.encode('utf-8'))
		data = ujson.loads(body)
		next_payload = ujson.dumps({'ct': data[1]})
		yield self.convert_json_data(data[0])
		yield scrapy.Request("https://myactivity.google.com/item?jspb=1", method="POST", cookies=cooks, body=next_payload, callback=self.parse, dont_filter=True)
	def convert_json_data(self, base_array):
		obj = {}
		for ele in base_array:

			#check to see if this was a page visited and not something else that google tracks such as keyword search or chrome app usage
			if ele[0][0][2] != 'Visited':
				continue
			obj['title'] = ele[0][0][0]
			#index of q=
			ind = ele[0][0][3].find('q=')
			obj['url'] = ele[0][0][3][(ind+2):]
			#index of next parameter
			ind = obj['url'].find('&')
			obj['url'] = obj['url'][:ind]
			#get the date
			d = str(datetime.fromtimestamp(int(ele[0][1])/1000000))
			obj['date'] = d

			obj['domain'] = ele[7][1]
			return obj
