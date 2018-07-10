import scrapy
import datetime
import json
from unicodedata import normalize


class RoomRentSpider(scrapy.Spider):
    name = "otodom_properties"

    def start_requests(self):
        url = "https://www.otodom.pl/i2/oferty/results/?json=1&limit=50&compact=1&view=list&search%5Bcity_id%5D=38&search%5Bcategory_id%5D=101&page=1"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ad_ids = [ ad["id"] for ad in json.loads(response.body.decode("utf-8"))["ads"] ]
        for ad_id in ad_ids:
            url = "https://www.otodom.pl/i2/oferta/?json=1&id=" + ad_id
            yield scrapy.Request(url=url, callback=self.parse_details)
        yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["next_page_url"], callback=self.parse)

    def parse_details(self, response):
        ad = json.loads(response.body.decode("utf-8"))
        yield {
                'title': normalize("NFKD", ad["title"]),
                'price': normalize("NFKD", ad["list_label"].replace("zł", "").replace(" ","") ),
                'area': ad["extra"]["m"]["value"].replace(" m²",""),
                'added_at': datetime.datetime.now(),
                'rooms': ad["extra"]["rooms_num"]["value"],
                'url': ad["url"],
                'description': normalize("NFKD",ad["description"]),
                'inactive': ad["status"] != "active",
                "sold_by": "unknown",
                "updated_at": datetime.datetime.now()
        }
