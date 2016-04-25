#!/usr/bin/env python
#-*- coding: utf-8 -*-


from multiprocessing import Pool
from item_links import get_link
from navi_url import navi_list
import pymongo,time


# client=pymongo.MongoClient('localhost',27017)
# ganji=client['ganji']
# item_link=ganji['item_link']
# page_list=[]
#
#
# # for item in item_link.find().sort('insert_time',pymongo.DESCENDING):    # This is type.Cursor,CANNOT use find_one
# #     page_list.append(item['page'])
# # print (type(page_list[0]-1))
# print (item_link.find_one()==None)


client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
item_info_lb = ganji['item_info_lb']


for item in item_info_lb.find().limit(5):
    print (item['address'].split('-'))