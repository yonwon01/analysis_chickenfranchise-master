import urllib
from datetime import datetime
from itertools import count
import xml.etree.ElementTree as et
import crawler
from bs4 import BeautifulSoup
import pandas as pd
from data_dict import sido_dict, gungu_dict
from selenium import webdriver
import time

RESULT_DIRECTORY = '../__result__/crawling'


def proc_bbq(html):
    bs = BeautifulSoup(html, 'html.parser')
    tag_tbody = bs.find('tbody')

    result = []
    for tag_tr in tag_tbody.findAll('tr'):
        strings = list(tag_tr.strings)

        name = strings[1]
        address = strings[3]
        sidogu = address.split()[:2]

        result.append((name, address) + tuple(sidogu))

    return result


def store_bbq(data):
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    # 중복 제거
    table = table.\
        drop_duplicates(subset='name', keep='first').\
        reset_index(drop=True)

    # 행정구역 정리
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/bbq_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_pelicana():

    result = []

    for page in count(start=1):

        url = 'http://www.pelicana.co.kr/store/stroe_search.html?page=%d' % page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})

        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)

            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]

            result.append((name, address) + tuple(sidogu))

    table = pd.DataFrame(result, columns=['name', 'address', 'sido', 'gungu'])

    # 중복 제거
    table = table.\
        drop_duplicates(subset='name', keep='first').\
        reset_index(drop=True)

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def proc_nene(xml):
    result = []

    root = et.fromstring(xml)
    for element in root.findall('item'):
        name = element.findtext('aname1')
        sido = element.findtext('aname2')
        gungu = element.findtext('aname3')
        address = element.findtext('aname5')

        result.append((name, address, sido, gungu))

    return result


def store_nene(data):
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    # 중복 제거
    table = table.\
        drop_duplicates(subset='name', keep='first').\
        reset_index(drop=True)

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/nene_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawl_kyochon():

    result = []

    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = crawler.crawling(url=url)

            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})

            for tag_a in tag_ul.findAll('a'):
                tag_dt = tag_a.find('dt')
                if tag_dt is None:
                    break

                name = tag_dt.get_text()

                tag_dd = tag_a.find('dd')
                if tag_dd is None:
                    break

                address = tag_dd.get_text().strip().split('\r')[0]
                sidogu = address.split()[:2]
                result.append((name, address) + tuple(sidogu))

    table = pd.DataFrame(result, columns=['name', 'address', 'sido', 'gungu'])

    # 중복 제거
    table = table.\
        drop_duplicates(subset='name', keep='first').\
        reset_index(drop=True)

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawl_goobne():
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    wd = webdriver.Chrome('D:/Python/webdriver/chromedriver.exe')
    wd.get("http://www.goobne.co.kr/store/search_store.jsp")
    time.sleep(5)

    result = []
    for page in count(start=1):
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print('%s : success for script execution (%s)' % (datetime.now(), script))
        time.sleep(5)

        html = wd.page_source
        bs = BeautifulSoup(html, 'html.parser')

        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)

            name = strings[1]
            address = strings[5] if strings[3] == '' else strings[6]
            sidogu = address.split()[:2]
            result.append((name, address) + tuple(sidogu))

    wd.quit()

    # store
    table = pd.DataFrame(result, columns=['name', 'address', 'sido', 'gungu'])

    # 중복 제거
    table = table.\
        drop_duplicates(subset='name', keep='first').\
        reset_index(drop=True)

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/goobne_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)



if __name__ == '__main__':

    # BBQ collection
    crawler.crawling(
        url='https://www.bbq.co.kr/shop/shop_ajax.asp?page=1&pagesize=2000&gu=&si=',
        proc=proc_bbq,
        store=store_bbq)

    # Pelicana collection
    crawling_pelicana()

    # NeNe collection
    crawler.crawling(
        url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'
            % (urllib.parse.quote('전체'), urllib.parse.quote('전체')),
        proc=proc_nene,
        store=store_nene)

    # Kyochon collection
    crawl_kyochon()

    # Goobne collection
    crawl_goobne()
