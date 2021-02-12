import scrapy

from scrapy.loader import ItemLoader
from ..items import BancaconsuliaItem
from itemloaders.processors import TakeFirst


class BancaconsuliaSpider(scrapy.Spider):
	name = 'bancaconsulia'
	start_urls = ['https://www.bancaconsulia.it/notizie/']

	def parse(self, response):
		year_links = response.xpath('//nav[@class="elementor-pagination"]/a/@href').getall()
		for link in year_links:
			yield response.follow(link, self.parse_page)

	def parse_page(self, response):
		post_links = response.xpath('//article//h1/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath(
			'//section[@class="elementor-element elementor-element-473a84d elementor-section-boxed elementor-section-height-default elementor-section-height-default elementor-section elementor-inner-section"]//div[@class="elementor-widget-container"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath(
			'//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()').get()

		item = ItemLoader(item=BancaconsuliaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
