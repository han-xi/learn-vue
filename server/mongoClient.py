from bson.codec_options import DEFAULT_CODEC_OPTIONS
from pymongo import MongoClient
import pymongo
from datetime import datetime


options = DEFAULT_CODEC_OPTIONS.with_options(
    unicode_decode_error_handler='ignore')
print('codec options ---', options.unicode_decode_error_handler)


class MongoDBClient233(object):
    def __init__(self, host='localhost', port=27017, db_name='info'):
        self.client = MongoClient(
            host, port, unicode_decode_error_handler='ignore')
        self.db = self.client.get_database(db_name, codec_options=options)
        print("233 mongo connected")
        self.info = self.db["info"]
        self.mail = self.db["mail"]
  
      