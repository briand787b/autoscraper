#!/usr/bin/env python3

from bs4 import BeautifulSoup
import httpx
import json
from parse import parse
from random import randint
import re
import sys
import time

# TODO:
# 1. Add realistic headers to scraper
# 2. Make scraper more resilient to failures

# query params
#
# number of records to retrieve
NUM_RECORDS_KEY = 'numRecords'
NUM_RECORDS_DEFAULT_VALUE = 100
# how many miles to search
SEARCH_RADIUS_KEY = 'searchRadius'
SEARCH_RADIUS_DEFAULT_VALUE = 250
# maximum price in USD
MAX_PRICE_KEY = 'maxPrice'
MAX_PRICE_DEFAULT_VALUE = 50_000
# how many records to skip
SKIP_KEY = 'firstRecord'

# scrape targets
#
# Trucks
TARGET_F150 = 'f150'
TARGET_SILVERADO = 'silverado'
TARGET_RAM = 'ram'
TARGET_TITAN = 'titan'
TARGET_TUNDRA = 'tundra'
TARGET_COLORADO = 'colorado'
TARGET_TACOMA = 'tacoma'
# SUVs
TARGET_EXPEDITION = 'expedition'
TARGET_TAHOE = 'tahoe'
TARGET_SUBURBAN = 'suburban'
# Cars
TARGET_458_SPYDER = '458_spyder'


def scrape_model(target: str):
    target = target.lower()
    if target == TARGET_F150:
        return f150()
    elif target == TARGET_458_SPYDER:
        return f458_spyder()
    else:
        raise Exception(f'scraper for {target} not implemented')


def f150():
    F150_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ford/f150/atlanta-ga-30338'
    inv_list = scrape_url(F150_4WD_URL)
    return inv_list


def f458_spyder():
    F458_SPYDER_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/ferrari/458-spider/atlanta-ga-30338'

    params = default_params()
    params[MAX_PRICE_KEY] = 500_000
    params[NUM_RECORDS_KEY] = 5
    print('about to scrape url')
    return scrape_url(F458_SPYDER_URL, params)


def titan():
    TITAN_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/nissan/titan/atlanta-ga-30338'
    inv_list = scrape_url(TITAN_4WD_URL)
    return inv_list


def default_params():
    return {
        NUM_RECORDS_KEY: NUM_RECORDS_DEFAULT_VALUE,
        SEARCH_RADIUS_KEY: SEARCH_RADIUS_DEFAULT_VALUE,
        MAX_PRICE_KEY: MAX_PRICE_DEFAULT_VALUE,
    }


def scrape_url(base_url: str, params: dict = default_params()):
    print('initial retrieval of records')
    resp = httpx.get(base_url, params=params)
    inv_list, next = scrape_doc(resp.text)

    while next:
        dur = randint(1, 10)
        print(f'scraping next page in {dur} secs')
        time.sleep(dur)
        params[SKIP_KEY] = next
        resp = httpx.get(base_url, params=params)
        next_list, next = scrape_doc(resp.text)
        inv_list += next_list

    return inv_list


def scrape_doc(document: str):
    DATA_LOC = 'window.__BONNET_DATA__'
    bs = BeautifulSoup(document, 'html.parser')
    data = bs.find('script', text=re.compile(DATA_LOC)).get_text()
    payload = data.split(DATA_LOC + '=')[1]
    with open('examples/output.json', 'w') as file:
        file.write(payload)

    return parse(json.loads(payload)), next(bs)


def next(bs: BeautifulSoup):
    tag_txt = bs.find('div',
                      {'class': 'results-text-container'},
                      text=re.compile('Results$'),
                      ).get_text()

    counts = tag_txt.strip().split('Results')[
        0].strip().replace(',', '').split(' of ')
    max = int(counts[1])
    end = int(counts[0].split('-')[1])
    if end < max:
        return end


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('ERROR: requires one url arg')

    scrape_url(sys.argv[1])
