#!/usr/bin/env python3

from bs4 import BeautifulSoup
import httpx
import json
import parse
import random
import re
import sys
import time

# TODO: Add realistic headers to scraper

JSON_ASSIGNMENT = 'window.__BONNET_DATA__'

# query params
#
# number of records to retrieve
NUM_RECORDS_KEY = 'numRecords'
NUM_RECORDS_DEFAULT_VALUE = 100
# how many miles to search
SEARCH_RADIUS_KEY = 'searchRadius'
SEARCH_RADIUS_DEFAULT_VALUE = 500
# maximum price in USD
MAX_PRICE_KEY = 'maxPrice'
MAX_PRICE_DEFAULT_VALUE = 50_000
# how many records to skip
SKIP_KEY = 'firstRecord'


def scrape_all():
    scrape_f150()


def scrape_f150():
    params = default_params()
    inv_list = scrape_url('base_f150_url', params)
    print(f'inv list will now be saved to database: {inv_list[-1]}')


def scrape_458_spyder():
    params = default_params()
    params[MAX_PRICE_KEY] = 500_000
    params[NUM_RECORDS_KEY] = 5
    print('about to scrape url')
    scrape_url(
        'https://www.autotrader.com/cars-for-sale/all-cars/ferrari/458-spider/atlanta-ga-30338',
        params,
    )


def default_params():
    return {
        NUM_RECORDS_KEY: NUM_RECORDS_DEFAULT_VALUE,
        SEARCH_RADIUS_KEY: SEARCH_RADIUS_DEFAULT_VALUE,
        MAX_PRICE_KEY: MAX_PRICE_DEFAULT_VALUE,
    }


def scrape_url(base_url: str, params: dict = {}):
    print('initial retrieval of records')
    resp = httpx.get(base_url, params=params)
    payload, next = scrape_doc(resp.text)
    inv_list = parse.parse(payload)

    while next:
        dur = random.randint(1, 10)
        print(f'scraping next page in {dur} secs')
        time.sleep(dur)
        params[SKIP_KEY] = next
        resp = httpx.get(base_url, params=params)
        payload, next = scrape_doc(resp.text)
        inv_list += parse.parse(payload)

    return inv_list


def scrape_doc(doc: str):
    bs = BeautifulSoup(doc, 'html.parser')
    data = bs.find('script', text=re.compile(JSON_ASSIGNMENT)).get_text()
    payload = data.split(JSON_ASSIGNMENT + '=')[1]
    with open('examples/output.json', 'w') as file:
        file.write(payload)

    return json.loads(payload), next(bs)


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


def test_scrape_doc():
    with open('examples/resp.html', 'r') as file:
        doc = file.read()

    return scrape_doc(doc)


def test_scrape_url():
    print('about to scrape 458 spyder records')
    scrape_458_spyder()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('ERROR: requires one url arg')

    scrape_url(sys.argv[1])
