import scrapy


class CreditagricoleroItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
