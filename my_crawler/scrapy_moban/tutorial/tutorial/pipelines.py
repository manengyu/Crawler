# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json
import codecs
import MySQLdb
import traceback

class TutorialPipeline(object):
	def __init__(self):
		self.file = codecs.open('name', mode='wb', encoding='utf-8')
		
    def process_item(self, item, spider):
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line.decode('unicode_escape'))
        return item
	# 连接数据库
	@staticmethod
	def connect_database(db_nick=''):
		if db_nick == 'Data':
			while True:
				try:
					conn = MySQLdb.connect(host='192.168.16.17', user='', passwd='',
										   db='Data', port=3306, charset='utf8')
					break
				except MySQLdb.Error, e:
					print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		else:
			print 'No such database!!!'
		return conn
		
	@staticmethod
    def insert_bid(conn, cur, ):
        insert_sql = u"INSERT " +  + u"() VALUES ('" ++ u"')"
        try:
            cur.execute(insert_sql)
            conn.commit()
        except MySQLdb.Error:
            traceback.print_exc()
    
    @staticmethod
    def insert_borrow(conn, cur, ):
        insert_sql = u"INSERT " +  + u"() VALUES('" + + u"')"
        try:
            cur.execute(insert_sql)
            conn.commit()
        except MySQLdb.Error:
            traceback.print_exc()
