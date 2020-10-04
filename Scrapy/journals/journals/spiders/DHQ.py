import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "dhq"
    start_urls = [
        'http://www.digitalhumanities.org/dhq/vol/13/4/index.html'
    ]
    
    def parse(self, response):
       
        body = response.xpath("/html/body")

        articles = body.xpath('//div[@class="articleInfo"]')

        return [
                {
                    "title": article.xpath('.//a/text()').get(),
                    "authors": [
                        {
                            "full-name": author.split(",")[0],
                            "affiliations": author.split(",", 1)[1],
                        }
                        for author in article.xpath('.//div/text()').get().split(";")
                    ],
                    "abstract": article.xpath('.//span/span[2]/text()').get()
                }
                for article in articles
                ]
            
""" 
        parsed = {
                'titles': body.xpath('//div[@class="articleInfo"]/a/text()').getall(),
                'authors-affiliations': body.xpath('//div[@class="articleInfo"]/div/text()').getall(),
                'abstracts': body.xpath('//div[@class="articleInfo"]/span/span[2]/text()').getall() 
                }

        articles = [{
            "title": parsed["titles"][i],
            "authors-affiliation": parsed["authors-affiliations"][i],
            "abstract": parsed["abstracts"][i],
        } for i in range(len(parsed["titles"]))]

        return articles """