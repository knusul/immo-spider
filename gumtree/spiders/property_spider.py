import scrapy
from unicodedata import normalize


class QuotesSpider(scrapy.Spider):
    name = "properties"

    def start_requests(self):
        urls = [
            'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/krakow/v1c9073l3200208p1',
#            'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/krakow/page-641/v1c9073l3200208p641'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.css('.result-link a::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_details)
        next_page = response.css("a.next.follows::attr(href)").extract_first()
        if next_page is not None:
          next_page = response.urljoin(next_page)
          yield scrapy.Request(next_page, callback=self.parse)


    def parse_details(self, response):
        yield {
                'title': normalize("NFKD", response.css("span.myAdTitle::text").extract_first()),
                'price': normalize("NFKD", response.css("span.amount::text").extract_first().replace(u'\xa0', '') ),
                'area': response.xpath("//*[text()='Wielkość (m2)']/parent::*").css('span.value::text').extract_first(),
                'rooms': response.xpath("//*[text()='Liczba pokoi']/parent::*").css('span.value::text').extract_first(),
                'url': response.url
        }
