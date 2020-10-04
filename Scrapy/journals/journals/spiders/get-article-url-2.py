import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "get-article-url-2"
    start_urls = [
        'https://www.euppublishing.com/toc/ijhac/12/2'
    ]
    
    def parse(self, response):
        yield {
                'doi': response.xpath('//*[text() = "Abstract"]/@href').getall()
                }
        """ for article_card in response.xpath("/html/body"):
            print("\n\n\n\n\n")
            print(article_card.xpath('//a[@class="ref nowrap abs"]/text()').getall())
        for item in response.xpath('//a[@class="ref nowrap abs"]/text()').getall() = Abstract: 
            if item == 'Abstract':
                print("CCCIIIAAAOOO") """
                 

              #   //div[@class="art_title linkable"]/a/@href