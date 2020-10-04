import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://umanisticadigitale.unibo.it/article/view/9975'
    ]

    def parse(self, response):
        for article in response.xpath('/html/head'):
            yield {
                'title': article.xpath('//meta[@name="DC.Title"]/@content').get(),
                'keywords': article.xpath('//meta[@name="DC.Subject"]/@content').getall(),
                'author': article.xpath('//meta[@name="DC.Creator.PersonalName"]/@content').getall(),
                'abstract': article.xpath('//meta[@name="DC.Description"][lang("en")]/@content').get(),
                'DOI': article.xpath('//meta[@name="DC.Identifier.DOI"]/@content').get(),
                'affiliation': article.xpath('//meta[@name="citation_author_institution"]/@content').getall(),
                'journal': article.xpath('//meta[@name="DC.Source"]/@content').get(),
                'issue': article.xpath('//meta[@name="DC.Source.Issue"]/@content').get()
            }
"""         next_article_url = response.css("li.next > a::attr(href)").get()
        if next_article_url is not None:
            yield scrapy.Request(response.urljoin(next_article_url)) """