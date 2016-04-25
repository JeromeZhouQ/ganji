#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
We connect navi_list from navi_url,
and then make-up the url we need,
channel,page,person or company

Maybe we could use multithreading for all-page link
Finally, we got all item link
'''

from navi_url import navi_list
from bs4 import BeautifulSoup
import time, requests, pymongo,random

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
item_link = ganji['item_link']




def get_item_link(url):
    return '' if url == [] else url.get('href')


def get_link(channel, page, whosell=1):  # 1 represent person
    page_link = '{}a{}o{}/'.format(channel, str(whosell), str(page))
    # print (page_link)
    try:
        webdata = requests.get(page_link)
        soup = BeautifulSoup(webdata.text, 'html.parser')
        # print (soup)
        if soup.find('ul', 'pageLink'):  # The last page
            item_links = soup.select('dd.feature > div > ul > li > a')
            # print(item_link)
            for item_url in item_links:
                time.sleep(random.uniform(0,1))
                data = {
                    'insert_time':time.time(),
                    'page': page,
                    'link': get_item_link(item_url)
                }
                # print(data)
                item_link.insert_one(data)
        else:
            pass
    except ConnectionError:
        time.sleep(random.randint(60,100))
        pass
    except ConnectionResetError:
        time.sleep(random.randint(100,120))
        pass
    except ConnectionAbortedError:
        time.sleep(random.randint(60,100))
        pass
    except requests.packages.urllib3.exceptions.ProtocolError:
        time.sleep(random.randint(60,100))
        pass
    except requests.exceptions.ConnectionError:
        time.sleep(random.randint(60,100))
        pass


