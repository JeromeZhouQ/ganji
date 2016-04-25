#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
We got all sencond-hand navi link and
put these in navi_list
'''

from bs4 import BeautifulSoup
import requests

link = 'http://bj.ganji.com/wu/'
navi_list = []


def get_text(link):
    part_link = 'http://bj.ganji.com'
    if link == []:
        return ''
    else:
        for i in range(0, len(link)):
            navi_list.append(part_link + (link[i].get('href')))
        return navi_list.remove('http://bj.ganji.com/shoujihaoma/')


webdata = requests.get(link)
soup = BeautifulSoup(webdata.text, 'html.parser')
url = soup.select('dl.fenlei > dt > a ')

get_text(url)
