import scrapy
import os
import psycopg2
import datetime
import json
from unicodedata import normalize
from dateutil.parser import parse

class OtodomRoomSpider(scrapy.Spider):
    custom_settings = {
	    'ITEM_PIPELINES': {
		'gumtree.pipelines.OtodomUpdater': 400
		}
	    }
    def __init__(self):
        hostname = os.environ["DB_HOSTNAME"]
        username = os.environ["DB_USERNAME"]
        password = os.environ["DB_PASSWORD"]
        database = os.environ["DB_DATABASE"]
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()
    name = "otodom_rooms_updater"

    def start_requests(self):
        ad_ids = self.cur.execute("""select external_id,added_at from properties WHERE external_id IS NOT NULL;""")
        ad_ids = [row for row in self.cur.fetchall()]
        print(ad_ids)
        for ad_id in ad_ids:
            url = "https://www.otodom.pl/i2/oferta/?json=1&id=" + str(ad_id[0])
            yield scrapy.Request(url=url, callback=self.parse_details, meta={'added_at':ad_id[1]})
    def parse_details(self, response):
        print(response.status)
        age = (datetime.datetime.now() - response.meta['added_at']).days
        ad = json.loads(response.body.decode("utf-8"))
        print(ad["status"])
        if(ad["status"]!= "active"):
            yield {
		    'price': normalize("NFKD", ad["list_label"].replace(" zł/mc", "").replace(" ","").replace(",",".")),
		    'created_at': datetime.datetime.now(),
		    'inactive': ad["status"] != "active",
		    'deactivated_at': datetime.datetime.now(),
		    "lat": float(ad["map_lat"]),
		    "lon": float(ad["map_lon"]),
		    "external_id": ad["id"],
		    'status': ad["status"],
		    "properties_id": ad["id"],
		    "age": age
		    }
