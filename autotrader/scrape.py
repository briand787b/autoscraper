#!/usr/bin/env python3

from bs4 import BeautifulSoup
import httpx
import json
from parse import parse
from random import randint
import re
import sys
import time


# query params
#
# number of listings to retrieve
NUM_RECORDS_KEY = 'numRecords'
NUM_RECORDS_DEFAULT_VALUE = 100
# how many miles to search
SEARCH_RADIUS_KEY = 'searchRadius'
SEARCH_RADIUS_DEFAULT_VALUE = 400
# maximum price in USD
MAX_PRICE_KEY = 'maxPrice'
MAX_PRICE_DEFAULT_VALUE = 40_000
# maximum number of miles
MAX_MILEAGE_KEY = 'maxMileage'
MAX_MILEAGE_DEFAULT_VALUE = 100_000
# how many records to skip
SKIP_KEY = 'firstRecord'
# Crew cab key/value pair
BODYSTYLE_SUBTYPE_KEY = 'bodyStyleSubtypeCodes'
BODYSTYLE_SUBTYPE_CREW_CAB = 'FULLSIZE_CREW+COMPACT_CREW'
# engine displacement range
ENGINE_DISPLACEMENT_KEY = 'engineDisplacement'
ENGINE_DISPLACEMENT_5L = '5.0-5.9'
# engine cylinders
ENGINE_CYL_KEY = 'engineCodes'
ENGINE_CYL_8 = '8CLDR'

# scrape targets
#
# Trucks
TARGET_COLORADO = 'colorado'
TARGET_F150 = 'f150'
TARGET_FRONTIER = 'frontier'
TARGET_RAM = 'ram'
TARGET_SIERRA = 'sierra'
TARGET_SILVERADO = 'silverado'
TARGET_TACOMA = 'tacoma'
TARGET_TITAN = 'titan'
TARGET_TUNDRA = 'tundra'
# SUVs
TARGET_EXPEDITION = 'expedition'
TARGET_GX460 = 'gx460'
TARGET_SEQUOIA = 'sequoia'
TARGET_SUBURBAN = 'suburban'
TARGET_TAHOE = 'tahoe'
# Minivans
TARGET_ODYSSEY = 'odyssey'
TARGET_SEDONA = 'sedona'
TARGET_SIENNA = 'sienna'


def all_targets():
    '''
    helper function for scrapes that target everything
    '''
    return [
        # Trucks
        TARGET_COLORADO,
        TARGET_F150,
        TARGET_FRONTIER,
        TARGET_RAM,
        TARGET_SIERRA,
        TARGET_SILVERADO,
        TARGET_TACOMA,
        TARGET_TITAN,
        TARGET_TUNDRA,
        # SUVs
        TARGET_EXPEDITION,
        TARGET_GX460,
        TARGET_SEQUOIA,
        TARGET_SUBURBAN,
        TARGET_TAHOE,
        # Minivans
        TARGET_ODYSSEY,
        TARGET_SEDONA,
        TARGET_SIENNA,
    ]

# Typical entrypoints


def scrape_model(target: str):
    '''
    scrape_model is useful for interfacing with a cli where the srape target
    is specified as a string arg
    '''
    target = target.lower()
    if target == TARGET_COLORADO:
        return colorado()
    elif target == TARGET_EXPEDITION:
        return expedition()
    elif target == TARGET_F150:
        return f150()
    elif target == TARGET_FRONTIER:
        return frontier()
    elif target == TARGET_GX460:
        return gx460()
    elif target == TARGET_ODYSSEY:
        return odyssey()
    elif target == TARGET_RAM:
        return ram()
    elif target == TARGET_SILVERADO:
        return silverado()
    elif target == TARGET_SEQUOIA:
        return sequoia()
    elif target == TARGET_SEDONA:
        return sedona()
    elif target == TARGET_SIENNA:
        return sienna()
    elif target == TARGET_SIERRA:
        return sierra()
    elif target == TARGET_SUBURBAN:
        return suburban()
    elif target == TARGET_TAHOE:
        return tahoe()
    elif target == TARGET_TACOMA:
        return tacoma()
    elif target == TARGET_TITAN:
        return titan()
    elif target == TARGET_TUNDRA:
        return tundra()
    else:
        raise Exception(f'scraper for {target} not implemented')


def colorado():
    COLORADO_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/colorado/atlanta-ga-30338'
    return scrape_url(COLORADO_4WD_URL, default_truck_params())


def expedition():
    EXPEDITION_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ford/expedition/atlanta-ga-30338'
    return scrape_url(EXPEDITION_4WD_URL, default_params())


def f150():
    F150_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ford/f150/atlanta-ga-30338'
    inv_list = scrape_url(F150_4WD_URL, default_truck_params())
    return inv_list


def frontier():
    FRONTIER_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/nissan/frontier/atlanta-ga-30338'
    return scrape_url(FRONTIER_4WD_URL, default_truck_params())


def gx460():
    GX460_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/lexus/gx-460/atlanta-ga-30338'
    return scrape_url(GX460_URL, default_params())


def odyssey():
    ODYSSEY_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/honda/odyssey/atlanta-ga-30338'
    return scrape_url(ODYSSEY_URL, default_params())


def ram():
    '''ignores V6 models'''
    RAM_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ram/1500/atlanta-ga-30338'
    params = default_truck_params()
    params[ENGINE_CYL_KEY] = ENGINE_CYL_8
    return scrape_url(RAM_4WD_URL, params)


def sedona():
    SEDONA_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/kia/sedona/atlanta-ga-30338'
    return scrape_url(SEDONA_URL, default_params())


def sienna():
    SIENNA_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/toyota/sienna/atlanta-ga-30338'
    return scrape_url(SIENNA_URL, default_params())

def sierra():
    SIERRA_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/gmc/sierra-1500/atlanta-ga-30338'
    return scrape_url(SIERRA_URL, default_truck_params())

def sequoia():
    SEQUOIA_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/toyota/sequoia/atlanta-ga-30338'
    return scrape_url(SEQUOIA_4WD_URL, default_params())


def silverado():
    SILVERADO_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/silverado-1500/atlanta-ga-30338'
    return scrape_url(SILVERADO_4WD_URL, default_truck_params())


def suburban():
    SUBURBAN_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/suburban/atlanta-ga-30338'
    return scrape_url(SUBURBAN_4WD_URL, default_params())


def tacoma():
    TACOMA_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/toyota/tacoma/atlanta-ga-30338'
    return scrape_url(TACOMA_4WD_URL, default_truck_params())


def tahoe():
    TAHOE_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/tahoe/atlanta-ga-30338'
    return scrape_url(TAHOE_4WD_URL, default_params())


def titan():
    TITAN_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/nissan/titan/atlanta-ga-30338'
    return scrape_url(TITAN_4WD_URL, default_truck_params())


def tundra():
    TUNDRA_4WD_URL = 'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/toyota/tundra/atlanta-ga-30338'
    return scrape_url(TUNDRA_4WD_URL, default_truck_params())


# Internal functions

def default_params():
    '''
    Query string parameters that apply to almost all listing searches
    '''
    return {
        NUM_RECORDS_KEY: NUM_RECORDS_DEFAULT_VALUE,
        SEARCH_RADIUS_KEY: SEARCH_RADIUS_DEFAULT_VALUE,
        MAX_PRICE_KEY: MAX_PRICE_DEFAULT_VALUE,
        MAX_MILEAGE_KEY: MAX_MILEAGE_DEFAULT_VALUE,
    }


def default_truck_params():
    '''Searches for crew cabs ONLY'''
    parms = default_params()
    parms[BODYSTYLE_SUBTYPE_KEY] = BODYSTYLE_SUBTYPE_CREW_CAB
    return parms


def scrape_url(base_url: str, params: dict):
    '''Scrapes specified AutoTrader URL'''
    resp = send_req(base_url, params)
    inv_list, next_skip = scrape_doc(resp)

    while next_skip:
        dur = randint(10, 60)
        print(f'scraping next page in {dur} secs')
        time.sleep(dur)
        params[SKIP_KEY] = next_skip
        resp = send_req(base_url, params)
        next_list, next_skip = scrape_doc(resp)
        inv_list += next_list

    with open('diags/inventory_list.json', 'w') as file:
        json.dump(inv_list, file)

    return inv_list


def send_req(base_url: str, params: dict):
    client = httpx.Client(timeout=120)  # long, but not infinite
    req = httpx.Request('GET', base_url, params=params, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',

    })
    print(f'[DEBUG] about to send request: {req}')
    resp = client.send(req)
    with open('diags/response.html', 'w') as file:
        file.write(resp.text)

    if resp.status_code > 299:
        raise Exception(f'request failed with status code: {resp.status_code}')

    return resp.text


def scrape_doc(document: str):
    '''Scrapes an AutoTrader HTML document containing vehicle search results '''
    DATA_LOC = 'window.__BONNET_DATA__'
    bs = BeautifulSoup(document, 'html.parser')
    data = bs.find('script', text=re.compile(DATA_LOC)).get_text()
    payload = data.split(DATA_LOC + '=')[1]
    with open('diags/response_data.json', 'w') as file:
        file.write(payload)

    payload_json = json.loads(payload)
    return parse(payload_json), next_skip(bs)


def next_skip(bs: BeautifulSoup):
    '''
    Calculates how many records to skip, if any, in next HTTP request.
    Returns None when no more records can be retrieved
    '''
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
