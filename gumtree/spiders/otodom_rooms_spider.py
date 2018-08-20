import scrapy
import datetime
from time import gmtime, strftime
import json
from unicodedata import normalize
import locale
import time
locale.setlocale(locale.LC_TIME, 'pl_PL.utf-8')


class OtodomRoomSpider(scrapy.Spider):
    name = "otodom_rooms"

    def start_requests(self):
        url = "https://www.otodom.pl/i2/ads/results/?json=1&limit=50&compact=1&view=list&search[city_id]=38&search[subregion_id]=410&search[category_id]=302&search[region_id]=6&search[order]=quality_score"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ad_ids = [ ad["id"] for ad in json.loads(response.body.decode("utf-8"))["ads"] ]
        for ad_id in ad_ids:
            url = "https://www.otodom.pl/i2/oferta/?json=1&id=" + ad_id
            yield scrapy.Request(url=url, callback=self.parse_details)
        yield scrapy.Request(url=json.loads(response.body.decode("utf-8"))["next_page_url"], callback=self.parse)

    def parse_details(self, response):
        ad = json.loads(response.body.decode("utf-8"))
        today_m = int(datetime.datetime.today().strftime("%m"))
        if ad["created"].find("dzisiaj"):
            ad_date =  datetime.datetime.now().timetuple()
        else:
            ad_date =  datetime.datetime.strptime(ad["created"], '%d %b').timetuple()

        ad_m = int(strftime("%m", ad_date))
        if( today_m > ad_m):
            year  = int(datetime.datetime.today().strftime("%Y")) - 1
        else:
            year  = int(datetime.datetime.today().strftime("%Y"))

        yield {
                'title': normalize("NFKD", ad["title"]),
                'price': normalize("NFKD", ad["list_label"].replace(" zł/mc", "").replace(" ","").replace(",",".")),
                'added_at': datetime.datetime.now(),
                'url': ad["url"],
                'description': normalize("NFKD",ad["description"]),
                'inactive': ad["status"] != "active",
                "sold_by": "unknown",
                "updated_at": datetime.datetime.now(),
                "area": None,
                "rooms": None,
                "lat": float(ad["map_lat"]),
                "lon": float(ad["map_lon"]),
                "source": "otodom-rooms",
                "external_id": ad["id"],
                "created_at": ad_date.replace(year=year)
        }
