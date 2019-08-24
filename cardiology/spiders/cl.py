import scrapy
from bs4 import BeautifulSoup
from itertools import chain
from cardiology.items import CardiologyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class cly_cl(CrawlSpider):
	name = "cardiology"
	start_urls = ['https://www.hindawi.com/journals/cric/contents/1/']
	rules = [
		Rule(LinkExtractor(allow=('/journals/cric/contents/[1-3]$')), callback='parse', follow=True),
	]
	def parse(self, response):
		domain = 'https://www.hindawi.com'
		sp = BeautifulSoup(response.body)
		sp1 = sp.select('.middle_content')

		s2 = [s.find_all('a') for s in sp1]
		s3 = [s.text.split(',') for s in s2[0]]
		s4=list(chain(*s3[:-1]))
		l=(len(s4))

		sp3=[]
		for k in range(l-3):
		    sp2 = [s.select('a')[k]['href'] for s in sp1]
		    sp3.append(sp2)
		    
		sp4=[]
		for i in sp3:
		    if (len(str(i))-4) == 28:
		        sp4.append(i)
		    else:
		        continue
		sp5=list(chain(*sp4))
		for e in sp5:
			yield scrapy.Request(domain + e, self.parse_detail)

	def parse_detail(self, response):
		d = BeautifulSoup(response.body)
		carditem = CardiologyItem()
		d2 = d.select('.middle_content')
		p = [s.select('h2') for s in d2]
		for pe in p[0]:
		    carditem['title'] = pe.text

		d3 = [s.select('p') for s in d2]
		d4 = [s.text for s in d3[0]]
		cont =''
		for t in d4:
		    cont += t
		carditem['content'] = cont

		return carditem
