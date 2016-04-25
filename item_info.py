#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This we will parser all imformation from ganji
But we will operate all 20 sets page
there, we firstly spider from "link" : "http://bj.ganji.com/jiaju/1967792925x.htm"
And we also recognize the invalid web_page
'''

from bs4 import BeautifulSoup
import requests, time, pymongo,random

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
item_info_lb = ganji['item_info_lb']
item_link = ganji['item_link']

headers = {
    'cookie': 'citydomain=bj; ganji_uuid=5102723755684574825204; '
              'ganji_xuuid=7dba95fc-eb95-4d59-bba8-4c6b0752e21d.1461372672155; '
              'GANJISESSID=51e7337376c84ad1bdc0d72335688dc7; __utma=32156897.1613697947.1461372616.1461378125.1461389813.3; '
              '__utmb=32156897.3.10.1461389813; __utmc=32156897; __utmz=32156897.1461372616.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); lg=1;'
              ' _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A37324622272%7D',
    'referer': 'http://bj.ganji.com/jiaju/1967792925x.htm',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}


def get_text(item):
    return '' if item == [] else ''.join(
        item[0].get_text().strip().replace(' ', '').replace('\r', '').replace('\n', ''))

def get_use(item):
    return '' if item == [] else ''.join(
        item[0].get_text().strip().replace(' ', '').replace('\r', '').replace('\n', '')).replace('新旧程度：','')


def get_view(link):
    id = link.split('/')[-1]
    url = 'http://analytics.ganji.com/rta/?gjch=/wu/jiaju/chuangdian/detail@post_id=26942278@agent=1@ad_type=2@source_type=0@' \
          'puid=1967792925&refer=http%3A%2F%2Fbj.ganji.com%2Fjiaju%' + id
    webdata = requests.get(url, headers=headers)
    if webdata.text.find('value'):  # Beautiful(webdata.text,'html.parser') We cannt find value
        return (webdata.text.split(':')[-1].replace('}', ''))
    else:
        return ('')


def get_item_info(link):
    time.sleep(random.uniform(0,3))    #随机休息
    try:
        webdata = requests.get(link, headers=headers)
        if webdata.status_code == 200:
            soup = BeautifulSoup(webdata.text, 'html.parser')
            title = soup.title.text
            post_time = soup.select('i.pr-5')
            views = get_view(link)
            type = soup.select('ul.det-infor > li > span > a ')
            price = soup.select(' i.f22.fc-orange.f-type ')
            address = soup.select('ul.det-infor > li')
            address_str = '' if address[2] == 0 else address[2].get_text().replace(' ', '').replace('\r', '').replace('\n',
                                                                                                                      '').replace(
                '\xa0', '')[5:]
            use = soup.select('div.second-dt-bewrite > ul > li ')

            data = {
                'link': link,
                'title': title,
                'post_time': get_text(post_time)[:-3],
                'views': views,
                'price': get_text(price),
                'type': get_text(type),
                'address': address_str,
                'use': get_use(use)[:get_use(use).find('新')+1]
            }
            item_info_lb.insert_one(data)
        else:
            print('{} has some problems,please try again later'.format(link))
            pass
    except Exception as e:
        print (Exception,':',e)



if item_info_lb.find_one() == None:# 判断数据库中是否有元素
    print ('Start')
    for item in item_link.find():
        get_item_info(item['link'])
else:
    lb_links=[item['link'] for item in item_link.find()]
    info_links=[item['link'] for item in item_info_lb.find()]
    x=set(lb_links)
    y=set(info_links)
    rest_links=x-y
    for item in list(rest_links):
        get_item_info(item)

