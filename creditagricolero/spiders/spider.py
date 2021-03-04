import scrapy

from scrapy.loader import ItemLoader
from ..items import CreditagricoleroItem
from itemloaders.processors import TakeFirst


class CreditagricoleroSpider(scrapy.Spider):
	name = 'creditagricolero'
	start_urls = ['https://credit-agricole.ro/centrul-de-presa/']

	def parse(self, response):
		post_links = response.xpath('//h2[@class="entry-title"]/a')
		for post in post_links:
			url = post.xpath('./@href').get()
			title = post.xpath('./text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'title': title})

		next_page = response.xpath('//div[@class="alignleft"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response, title):
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=CreditagricoleroItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
