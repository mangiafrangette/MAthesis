import scrapy
import csv
import os
import json


class ArticlesSpider(scrapy.Spider):
    name = "data_mining"

    def start_requests(self):
        #urls = ["http://arxiv.org/abs/1312.5817v3"]
        #urls = ["https://hal.archives-ouvertes.fr/hal-02513038v2"]
        urls = [
            "https://hal.archives-ouvertes.fr/hal-02280013v2",
            "http://arxiv.org/abs/1912.05082v3",
            "https://hal.archives-ouvertes.fr/hal-02520508v3",
            "https://hal.archives-ouvertes.fr/hal-01913435v3",
            "https://hal.archives-ouvertes.fr/hal-01915730v2",
            "https://hal.archives-ouvertes.fr/hal-02109972v2",
            "https://hal.archives-ouvertes.fr/hal-02513038v2",
            "http://arxiv.org/abs/1602.08715v2",
            "https://hal.archives-ouvertes.fr/hal-01671592v1",
            "https://hal.archives-ouvertes.fr/hal-01283638v2",
            "https://hal.archives-ouvertes.fr/hal-01281266v2",
            "https://hal.archives-ouvertes.fr/hal-01528092v2",
            "https://hal.archives-ouvertes.fr/hal-01287195v4",
            "https://hal.archives-ouvertes.fr/halshs-01543050v2",
            "https://hal.archives-ouvertes.fr/hal-01294158v2",
            "https://hal.archives-ouvertes.fr/hal-01265297v2",
            "http://arxiv.org/abs/1602.08844v2",
            "http://arxiv.org/abs/1603.01597v2",
            "http://arxiv.org/abs/1602.08657v2",
            "https://hal.archives-ouvertes.fr/hal-01276243v3",
            "https://hal.archives-ouvertes.fr/hal-01279493v2",
            "http://arxiv.org/abs/1603.01207v1",
            "https://hal.archives-ouvertes.fr/halshs-01557447v1",
            "https://hal.archives-ouvertes.fr/hal-01371751v3",
            "https://hal.archives-ouvertes.fr/halshs-01532877v2",
            "https://hal.archives-ouvertes.fr/hal-01294591v2",
            "https://hal.archives-ouvertes.fr/hal-01645124v2",
            "https://hal.archives-ouvertes.fr/hal-01280627v4",
            "https://hal.archives-ouvertes.fr/hal-01282568v4",
            "https://hal.archives-ouvertes.fr/hal-01759191v2",
            "https://hal.archives-ouvertes.fr/hal-01762730v5",
            "https://hal.archives-ouvertes.fr/hal-01466986v2",
            "https://hal.archives-ouvertes.fr/hal-01458216v1",
            "https://hal.archives-ouvertes.fr/hal-01456090v2",
            "https://hal.archives-ouvertes.fr/hal-01443713v1",
            "https://hal.archives-ouvertes.fr/hal-01466986v1",
            "http://arxiv.org/abs/1312.6675v2",
            "http://arxiv.org/abs/1402.2003v2",
            "https://hal.archives-ouvertes.fr/hal-00919370v3",
            "http://arxiv.org/abs/1312.5817v3",
            "http://arxiv.org/abs/1312.4617v2",
            "http://arxiv.org/abs/1311.5401v2",
            "https://hal.archives-ouvertes.fr/hal-01024985v4",
            "http://arxiv.org/abs/1010.0803v3",
            "http://arxiv.org/abs/1405.3539v3",
            "https://hal.archives-ouvertes.fr/hal-01279493v2",
            "http://arxiv.org/abs/1808.10685v3",
            "https://hal.archives-ouvertes.fr/hal-02154122v2",
            "https://hal.archives-ouvertes.fr/hal-02324617v2",
            "http://arxiv.org/abs/2001.01863v7",
            "http://arxiv.org/abs/1807.04892v4",
            "https://hal.archives-ouvertes.fr/hal-01981922v3",
            "http://arxiv.org/abs/1801.00912v3"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # parse scrapy data
    def parse(self, response): 
        url = response.url
        affiliations = None
        issue = None
        issn_value = None
        issn_type = None
        publisher = None
        keywords = None
        volume = None
        authors_dicts_list = None
        sup = None
        struct_ids = None
        without_aff = None
        with_aff = None
        structs = None
        ids_set = None
        struct_ids_dict = None
        authors_ids_dict = None
        if "https://arxiv.org" in url:
            id_scheme = "arXiv"
            string_id = response.xpath('//meta[@name="citation_arxiv_id"]/@content').get()
            abstract = response.xpath('//*[@id="abs"]/blockquote').get()
            article_title = response.xpath('//*[@id="abs"]/h1').get()
            # no affiliation anywhere
            authors = response.xpath('//meta[@name="citation_author"]/@content').getall()
            date = response.xpath('//meta[@name="citation_date"]/@content').get()
            authors_dicts_list = [
                {'given': author.split(", ")[0],
                    'family': author.split(", ")[1],
                    'affiliations': None
                 }
                for author in authors
            ]
        else:
            id_scheme = "hal"
            string_id = response.xpath('//meta[@name="DC.identifier"][2]/@content').get()
            abstract = response.xpath('//div[@class="abstract-content"]').get()
            article_title = response.xpath('//h1[@class="title"]/text()').get()
            authors = response.xpath('//meta[@name="citation_author"]/@content').getall()
            affiliations = response.xpath('meta[@name="citation_author_institution"]').getall()
            date = response.xpath('//meta[@name="citation_online_date"]/@content').get()
            keywords = response.xpath('//meta[@name="citation_keywords"]/@content').getall()
            volume = response.xpath('//meta[@name="citation_volume"]/@content').get()

            with_aff = response.xpath('//span[sup and @class="author"]/a/text()').getall()
            authors_ids = response.xpath('//span[@class="author"]/sup/text()').getall()
            authors_ids = [ids.split(", ") for ids in authors_ids]
            ids_set = set()
            for ids in authors_ids:
                ids_set.update(set(ids))
            #without_aff = response.xpath('//span[not(sup) and @class="author"]/a/text()').getall()
            struct_ids_dict = {id: response.xpath(f'//div[span={id}]/a/text()').get() for id in ids_set}

            authors_ids_dict = {author: authors_ids[index] for index, author in enumerate(with_aff)}
            authors_dicts_list = []
            for author in authors:
                author_dict = {
                    'given': author,
                    'family': None,
                    'affiliations': None
                }
                if author in with_aff:
                    author_dict['affiliations'] = [struct_ids_dict[struct_id] for struct_id in authors_ids_dict[author]]
                authors_dicts_list.append(author_dict)


        yield {
        "url": url,
        "identifier": {
            "string_id": string_id,
            "id_scheme": id_scheme
        },
        "abstract": abstract,
        "article_title": article_title,
        "authors": authors_dicts_list,
        #  "authors": [
        # {
        # 'given': author,
        # 'family' : "",
        # 'affiliation' : []
        # }
        # for author in authors
        # ],
        "publisher": publisher,
        "date": date,
        "keywords": keywords,
        "journal_title": "Journal of Data Mining & Digital Humanities",
        "volume": volume,
        "issue": issue,
        "ISSN": [
            {
                "value": issn_value,
                "type": issn_type
            }
        ]
    }


                    
    
            


