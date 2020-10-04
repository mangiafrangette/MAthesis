import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "get-article-url-oxford"
    start_urls = [
        'https://academic.oup.com/dsh/search-results?f_TocHeadingTitle=Original+Articles&f_ArticleTypeDisplayName=Research+Article&fl_SiteID=5447&rg_ArticleDate=01%2f01%2f2000+TO+12%2f31%2f2020&page=1'
    ]
    
    def parse(self, response):
       
        for article_card in response.xpath("/html/body"):
            print(article_card.xpath('//div[@class="al-citation-list"]/span/a/@href')[0])
            """ if article_card.xpath('//p[@class="teaser-text"]/strong/text()').get() == "<strong>Original research</strong>":
                print("CCCIIIAAAOOO")
                yield {
                    'doi': article_card.xpath('//a[@class="article-DOI-link"]/@href').get()
                } """