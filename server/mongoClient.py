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
  
        # self.patent = self.db["patent"]

        # self.claim = self.db["claim"]

        # self.detail_desc_text = self.db["detail_desc_text"]
        # self.brf_sum_text = self.db["brf_sum_text"]

        # self.cpc_current = self.db["cpc_current"]
        # self.cpc_subgroup = self.db["cpc_subgroup"]
        # self.cpc_group = self.db["cpc_group"]

        # self.patent_inventor = self.db["patent_inventor"]
        # self.inventor = self.db["inventor"]

        # self.patent_assignee = self.db["patent_assignee"]
        # self.assignee = self.db["assignee"]

        # self.application = self.db['application']
        # self.foreign_priority = self.db['foreign_priority']
        # self.pct_data = self.db['pct_data']

        # self.foreigncitation = self.db['foreigncitation']
        # self.otherreference = self.db['otherreference']
        # self.usapplicationcitation = self.db['usapplicationcitation']
        # self.uspatentcitation = self.db['uspatentcitation']
