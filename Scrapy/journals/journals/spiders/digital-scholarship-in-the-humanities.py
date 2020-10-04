import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "digital-scholarship-in-the-humanities"
    start_urls = [
        'https://academic.oup.com/dsh/article/35/1/1/5308384'
    ]

    def parse(self, response):
        for article in response.xpath('/html/head'):
            yield {
                'title': article.xpath('//meta[@name="citation_title"]/@content').get(),
                'keywords': article.xpath('//meta[@name="citation_keywords"]/@content').getall(),
                'author': article.xpath('//meta[@name="citation_author"]/@content').getall(),
                'abstract': article.xpath('//meta[@name="citation_abstract"]/@content').get(),
                'DOI': article.xpath('//meta[@name="citation_doi"]/@content').get(),
                'affiliation': article.xpath('//meta[@name="citation_author_institution"]/@content').getall(),
                'journal': article.xpath('//meta[@name="citation_journal_title"]/@content').get(),
                'issue': article.xpath('//meta[@name="citation_volume"]/@content').get()
            }
"""         next_article_url = response.css("li.next > a::attr(href)").get()
        if next_article_url is not None:
            yield scrapy.Request(response.urljoin(next_article_url)) """