from gumtree.spiders.property_spider import PropertySpider
import scrapy
import psycopg2
import os

class UpdateSpider(PropertySpider):
  name = "update_property_spider"

  def get_urls(self):
      print("###########")
      hostname = os.environ["DB_HOSTNAME"]
      username = os.environ["DB_USERNAME"]
      password = os.environ["DB_PASSWORD"]
      database = os.environ["DB_DATABASE"]
      self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
      self.cur = self.connection.cursor()
      self.cur.execute("select url from properties where inactive = false;")
      rows = self.cur.fetchall()
      urls = [url for row in rows for url in row]
      return urls

  def start_requests(self):
      urls = self.get_urls()
      for url in urls:
          print("url is: " + url )
          yield scrapy.Request(url=url, callback=self.parse_details)
