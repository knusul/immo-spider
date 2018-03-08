import scrapy
from unicodedata import normalize


class QuotesSpider(scrapy.Spider):
    name = "properties"

    def start_requests(self):
        urls = [
            'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/krakow/v1c9073l3200208p1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.css('.result-link a::attr(href)').extract()
        for url in urls:
            print("URL:")
            print(url)
            yield scrapy.Request(response.urljoin(url), callback=self.parse_details)
        print("###### RESPONSE #####")
        print(response.body)
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse_details(self, response):
        yield {
                'title': normalize("NFKD", response.css("span.myAdTitle::text").extract_first()),
                'price': normalize("NFKD", response.css("span.amount::text").extract_first().replace(u'\xa0', '') ),
                'area': response.xpath("//*[text()='Wielkość (m2)']/parent::*").css('span.value::text').extract_first(),
                'rooms': response.xpath("//*[text()='Liczba pokoi']/parent::*").css('span.value::text').extract_first(),
        }
