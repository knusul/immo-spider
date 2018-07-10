# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import boto3
import psycopg2
import os
from colorama import Fore, Back, Style


class PostgresqlPipeline(object):
    def default_encoder(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        elif isinstance(value, datetime.time):
            return value.strftime('%H:%M:%S')
        else:
            return value


    def open_spider(self, spider):
        hostname = os.environ["DB_HOSTNAME"]
        username = os.environ["DB_USERNAME"]
        password = os.environ["DB_PASSWORD"]
        database = os.environ["DB_DATABASE"]
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        print("""insert into properties(title,price,area,added_at,sold_by,rooms,url,description,inactive,updated_at) values('%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s') ON CONFLICT(url) DO UPDATE SET visits = properties.visits + 1, price = EXCLUDED.price""" % (item['title'],item['price'],item['area'],self.default_encoder(item['added_at']),item['sold_by'],item['rooms'],item['url'],item['description'],item['inactive'],self.default_encoder(item['updated_at'])))
        try:
            self.cur.execute("""insert into properties(title,price,area,added_at,sold_by,rooms,url,description,inactive,updated_at) values('%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s') ON CONFLICT(url) DO UPDATE SET visits = properties.visits + 1, price = EXCLUDED.price, inactive= EXCLUDED.inactive""" % (item['title'],item['price'],item['area'],self.default_encoder(item['added_at']),item['sold_by'],item['rooms'],item['url'],item['description'],item['inactive'],self.default_encoder(item['updated_at'])))
        except psycopg2.Error as e:
            print(Fore.RED + 'ERROR IS')
            print(e.pgerror)
            print(Style.RESET_ALL)
        self.connection.commit()
        return item
