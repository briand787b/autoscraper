#!/usr/bin/env python3

from bs4 import BeautifulSoup
import httpx
import json
import re
import sys

# TODO: Add realistic headers to scraper

JSON_ASSIGNMENT = 'window.__BONNET_DATA__'


def scrape_f150():
    print()


def scrape(base_url: str, params: dict = {}):
    resp = httpx.get(base_url, params=params)
    return scrape_doc(resp.text)


def scrape_doc(doc: str):
    bs = BeautifulSoup(doc, 'html.parser')
    data = bs.find('script', text=re.compile(JSON_ASSIGNMENT)).get_text()
    payload = data.split(JSON_ASSIGNMENT + '=')[1]
    with open('examples/output.json', 'w') as file:
        file.write(payload)

    return payload


def test_scrape_doc():
    with open('examples/resp.html', 'r') as file:
        doc = file.read()

    return scrape_doc(doc)


def test_scrape_url():
    return scrape('https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ford/f150/atlanta-ga-30338?searchRadius=500&maxPrice=50000&numRecords=100')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('ERROR: requires one url arg')

    scrape(sys.argv[1])
