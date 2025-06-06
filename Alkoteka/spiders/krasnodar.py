import scrapy


class KrasnodarSpider(scrapy.Spider):
    name = "krasnodar"
    allowed_domains = ["alkoteka.com"]
    start_urls = ["https://alkoteka.com"]

    def parse(self, response):
        pass
