import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "get-doi"
    start_urls = [
        ''
    ]
    
    def parse(self, response):
        for article_card in response.xpath("/html/body"):
            print(article_card.xpath('//div[@class="ww-citation-primary"]/a/@href').get())
            yield {
                'doi': article_card.xpath('//div[@class="ww-citation-primary"]/a/@href').get()
            }