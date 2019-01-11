import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi
class GoogleFanyiPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item
    def handle_error(self, failure):
        print(failure)
    def do_insert(self, cursor, item):
        sql = """INSERT INTO fanyi(original, translation)
        VALUES(%s, %s)"""
        cursor.execute(sql, (item['original'], item['translation']))
