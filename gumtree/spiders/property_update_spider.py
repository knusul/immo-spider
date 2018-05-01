from gumtree.spiders.property_spider import PropertySpider
import scrapy
import psycopg2

class UpdateSpider(PropertySpider):
  name = "update_property_spider"

  def get_urls(self):
      print("###########")
      hostname = 'localhost'
      username = 'property'
      password = '' # your password
      database = 'properties'
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
