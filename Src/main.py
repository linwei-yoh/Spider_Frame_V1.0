#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'


from Mongo_Helper import MongoHelper
from RpSpider import RpSpider_Start
import pickle

if __name__ == '__main__':
    mongo_clent = MongoHelper()
    mongo_clent.insert_task([123, 'vic'])

    # 开始爬取
    RpSpider_Start()
