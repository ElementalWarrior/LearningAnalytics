
#
# import scrapy
# from scrapy.shell import inspect_response
# from scrapy.crawler import CrawlerProcess
# import logging
# from unidecode import unidecode
#
# class HistorySpider(scrapy.Spider):
# 	name = 'historyspider'
# 	start_urls = ['https://www.google-analytics.com/collect?v=1&_v=j47&a=921746042&t=pageview&_s=1&dl=https%3A%2F%2Fmyactivity.google.com%2Fitem&dp=%2Fstate%2Froot.timeline&ul=en-us&de=UTF-8&dt=Google%20-%20My%20Activity&sd=24-bit&sr=1920x1080&vp=1920x950&je=0&fl=23.0%20r0&_u=CACAAEABI~&jid=&cid=1588860801.1478368996&tid=UA-63711172-5&z=533185368']
#
# 	def parse(self, response):

import pycurl
import certifi
import zlib
from StringIO import StringIO

buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, "https://myactivity.google.com/item?jspb=1")
c.setopt(c.CAINFO, certifi.where())
c.setopt(c.HTTPHEADER, [
	"origin: https://myactivity.google.com"
	, "accept-encoding: gzip, deflate, br"
	, "accept-language: en-GB,en-US;q=0.8,en;q=0.6"
	, "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
	, "content-type: application/json;charset=UTF-8"
	, "accept: application/json, text/plain, */*"
	, "referer: https://myactivity.google.com/item"
	, "authority: myactivity.google.com"
	, "cookie: SID=8AMil81HmbBmRKz9jICeG7zh21EQ0vS5P1KQ7FZfjsWytHgwUZOuZFnnxJJDFwtg6AUNFQ.; HSID=AmbLwhFgJZj6PaAmX; SSID=ApuRse3ahji3APn6-; APISID=Ck72SDX2re2YIz13/AjGq5nqzn4zGD0pvq; SAPISID=_j8wZCldxi5OGdYv/ArJoZPvC1Mkk-AAcA; NID=90=Yf4PESgy5PeC6UL3JRmxYwf8FsAlsqa1SQoxNEMKpoblwczW_hUuhZ2JWSNte-8B6gqN_ilVUkAWodov5T4hBZivgQKddN-atHwdYcuBYwRvO8y69IcbEjrDFX3jlbkaTurH2gY9PjMoTOAyDA-8JuhgHjZk_G3oobO1NDeDM9rttAy14XRNzvH1KPwKTr6YyGRFImgxPSAbWmi2DNG0rS1d3eWzzYZrNiMVr18_-J2bOpBqIy-pTw; _gat=1; _ga=GA1.3.1588860801.1478368996"
	, "x-client-data: CIS2yQEIpLbJAQjEtskBCMKaygEIqZ3KAQ=="
])

#where to write the response data
c.setopt(c.WRITEDATA, buffer)
c.setopt(c.POSTFIELDS,'''{"ct":"AODP23YAAAEFCoICH4sIAAAAAAAAAOMS4GAUmNb5ilXi7ov1V3omXmDiAomcetHNJrHp392WfpAIPweTwIRFIRJX9095-2oCWAkzRNPNCw1_3vSDRdggIns-7nvfCVFTI3Ds01UpicNNky5NARkjyNHIKPDy2ytZiePrv-1phQg1MQr8nvMaRWgSo8DpiZ_kJP5vPrbvTD9YaAajwPR_p-UlPrx9PrMPomo31JWTH__aP38SWOgQo8CvK7dEJWbcOtfQD1F1Fqjx9hQVieal7_Zth5i1mEng1vsV-hJn3666PQui8RyTQMeyU3wSB-_N_jQXKCQwE2qCFBeHhACjBLtC00kVAOF3Jp8rAQAArg50IeSjGS3sTli8CA5UbADNA4w"}''')

c.perform()
c.close()


#decompress gzipped data response
actualData = zlib.decompress(buffer.getvalue(), 16+zlib.MAX_WBITS)
print actualData
# f = open ('file.txt', 'wb+')
# f.write(buffer.getvalue())
# f.close()
