#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
from item_links import get_link
from navi_url import navi_list

# print (navi_list)

def page_link_from(channel):
    for num in range(1,300):
        print (num)
        get_link(channel,num)

navi_list1=['http://bj.ganji.com/jiaju/', 'http://bj.ganji.com/rirongbaihuo/']

if __name__=='__main__':
    pool=Pool()
    pool.map(page_link_from,navi_list1)
