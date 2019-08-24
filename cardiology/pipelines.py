# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class CardiologyPipeline(object):
	def open_spider(self, spider):
		self.conn = sqlite3.connect('cardiology.sqlite')
		self.cur = self.conn.cursor()
		self.cur.execute('create table if not exists cardiology(title varchar(200), content text)')

	def close_spider(self, spider):
		self.conn.commit()
		self.conn.close()

	def process_item(self, item, spider):
		col = ','.join(item.keys())
		placeholders = ','.join(len(item) * '?')
		sql = 'insert into cardiology({}) values({})'
		self.cur.execute(sql.format(col, placeholders), tuple(item.values()))
		return item
