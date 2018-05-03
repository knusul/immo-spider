import scrapy
import datetime
from unicodedata import normalize
from gumtree.items import GumtreeItem
import dateutil


class PropertySpider(scrapy.Spider):
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
            yield scrapy.Request(response.urljoin(url), callback=self.parse_details)
        next_page = response.css("a.next.follows::attr(href)").extract_first()
        if next_page is not None:
          next_page = response.urljoin(next_page)
          yield scrapy.Request(next_page, callback=self.parse)


    def parse_details(self, response):
        title = normalize("NFKD", response.css("span.myAdTitle::text").extract_first())
        price = int(''.join(list(filter(str.isdigit, normalize("NFKD", response.css("span.amount::text").extract_first().replace(u'\xa0', '') )))))
        area = response.xpath("//*[text()='Wielkość (m2)']/parent::*").css('span.value::text').extract_first() or "NULL"
        added_at = dateutil.parser.parse(response.xpath("//*[text()='Data dodania']/parent::*").css('span.value::text').extract_first().strip())
        sold_by = response.xpath("//*[text()='Na sprzedaż przez']/parent::*").css('span.value::text').extract_first()
        rooms = response.xpath("//*[text()='Liczba pokoi']/parent::*").css('span.value::text').extract_first()
        url = response.url
        description = normalize("NFKD",response.css('.description::text').extract_first()).strip()
        inactive = (len(response.css('.vip-similar-ads.top')) == 1 ) or response.status !=200
        updated_at = datetime.datetime.now()
        yield GumtreeItem(
            title=title,
            price=price,
            area=area,
            added_at=added_at,
            sold_by=sold_by,
            rooms=rooms,
            url=url,
            description=description,
            inactive=inactive,
            updated_at=updated_at
                )
