from bson.codec_options import DEFAULT_CODEC_OPTIONS
from pymongo import MongoClient
import pymongo
from datetime import datetime
from getsecertinfo import secert

options = DEFAULT_CODEC_OPTIONS.with_options(
    unicode_decode_error_handler='ignore')
print('codec options ---', options.unicode_decode_error_handler)


class MongoDBClient233(object):
    def __init__(self,host='localhost',port=27017,db_name='info'):
        server_info=secert()
        self.client = MongoClient(
            server_info.server['host'],  server_info.server['port'], unicode_decode_error_handler='ignore')
        self.db = self.client.get_database( server_info.server['db_name'], codec_options=options)
        print("233 mongo connected")
        self.info = self.db["info"]
        self.mail = self.db["mail"]
        self.operatinglog=self.db["operatinglog"]
  
      