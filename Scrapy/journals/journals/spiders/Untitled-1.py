def parse(self, response):
       
        body = response.xpath("/html/body")

        parsed = {
                'titles': body.xpath('//div[@class="articleInfo"]/a/text()').getall(),
                'authors-affiliations': body.xpath('//div[@class="articleInfo"]/div/text()').getall(),
                'abstracts': body.xpath('//div[@class="articleInfo"]/span/span[2]/text()').getall() 
                }

        articles = [{
            "title": parsed["titles"].titles[i]
        } for i in range(len(parsed["titles"]))]

        yield articles