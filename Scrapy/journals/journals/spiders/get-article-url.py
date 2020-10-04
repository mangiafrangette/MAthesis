import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "get-article-url"
    start_urls = [
        'https://www.frontiersin.org/journals/digital-humanities#articles'
    ]
    
    def parse(self, response):
       
        for article_card in response.xpath("/html/body"):
            print("CCCIIIAAAOOO")
            print(article_card.xpath('//strong'))
            if article_card.xpath('//p[@class="teaser-text"]/strong/text()').get() == "<strong>Original research</strong>":
                print("CCCIIIAAAOOO")
                yield {
                    'doi': article_card.xpath('//a[@class="article-DOI-link"]/@href').get()
                }