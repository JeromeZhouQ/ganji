#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
from item_links import get_link
from navi_url import navi_list
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
item_link = ganji['item_link']

# navi_list1=['http://bj.ganji.com/jiaju/',
# 'http://bj.ganji.com/rirongbaihuo/']


def page_link_from(page):
    page_list = []
    print(page,'--------------------------------------------------------')
    if item_link.find_one() == None:  # 判断数据库中是否有元素
        for item in navi_list:
            get_link(item,page)
    else:  # 若有元素则进行断点续传
        for item in item_link.find().sort('insert_time', pymongo.DESCENDING):  # This is type.Cursor,CANNOT use find_one
            page_list.append(item['page'])
            if page_list[0]=='1':
                for num in range(1, 200):
                    for item in navi_list:
                        get_link(item, num)
            else:
                for num in range(page_list[0], 200):
                    for item in navi_list:
                        get_link(item, num)


if __name__ == '__main__':
    for page in range(1,200):
        page_link_from(page)
