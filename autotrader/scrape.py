from bs4 import BeautifulSoup
import httpx
import json
from parse import parse
from random import randint
import re
import sys
import time


# TODO:
# make the saving of responses in diags/ optional
# vary the ordering of cities to make scrapes look more random
# vary the ordering of models to make scrapes look more random
# rename TARGET to MODEL

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
MAX_MILEAGE_DEFAULT_VALUE = 150_000
# how many records to skip
SKIP_KEY = 'firstRecord'
# earliest year to search for
MIN_YEAR_KEY = 'startYear'
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
# # Minivans
TARGET_ODYSSEY = 'odyssey'
# TARGET_SEDONA = 'sedona'
TARGET_SIENNA = 'sienna'


# scrape regions
REGION_ATLANTA = 'atlanta-ga-30338'
REGION_BROOKFIELD = 'brookfield-ct-06804'
REGION_CHICAGO = 'chicago-il-60652'
REGION_KANSAS_CITY = 'kansas-city-mo-64101'
REGION_MIAMI = 'miami-fl-33101'
REGION_RALEIGH = 'raleigh-nc-27601'


def all_models():
    '''helper function for scrapes that target all models'''
    return (
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
        # # Minivans
        # TARGET_ODYSSEY,
        # TARGET_SEDONA,
        # TARGET_SIENNA,
    )


def all_regions():
    '''helper function for scrapes that search all regions'''
    return (
        REGION_ATLANTA,
        REGION_BROOKFIELD,
        REGION_CHICAGO,
        REGION_KANSAS_CITY,
        REGION_MIAMI,
        REGION_RALEIGH,
    )

# Typical entrypoints


def scrape_model(target: str, region: str):
    '''
    scrape_model is useful for interfacing with a cli where the srape target
    is specified as a string arg
    '''
    if region not in all_regions():
        raise Exception(f'unknown region: {region}')

    print(f'now scraping {target} in {region}')

    target = target.lower()
    if target == TARGET_COLORADO:
        return colorado(region)
    elif target == TARGET_EXPEDITION:
        return expedition(region)
    elif target == TARGET_F150:
        return f150(region)
    elif target == TARGET_FRONTIER:
        return frontier(region)
    elif target == TARGET_GX460:
        return gx460(region)
    elif target == TARGET_ODYSSEY:
        return odyssey(region)
    elif target == TARGET_RAM:
        return ram(region)
    elif target == TARGET_SILVERADO:
        return silverado(region)
    elif target == TARGET_SEQUOIA:
        return sequoia(region)
    # elif target == TARGET_SEDONA:
    #     return sedona(region)
    elif target == TARGET_SIENNA:
        return sienna(region)
    elif target == TARGET_SIERRA:
        return sierra(region)
    elif target == TARGET_SUBURBAN:
        return suburban(region)
    elif target == TARGET_TAHOE:
        return tahoe(region)
    elif target == TARGET_TACOMA:
        return tacoma(region)
    elif target == TARGET_TITAN:
        return titan(region)
    elif target == TARGET_TUNDRA:
        return tundra(region)
    else:
        raise Exception(f'scraper for {target} not implemented')


def colorado(region: str):
    COLORADO_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/colorado/{region}'
    return scrape_url(COLORADO_4WD_URL, default_truck_params())


def expedition(region: str):
    EXPEDITION_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ford/expedition/{region}'
    return scrape_url(EXPEDITION_4WD_URL, default_suv_params())


def f150(region: str):
    F150_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ford/f150/{region}'
    inv_list = scrape_url(F150_4WD_URL, default_truck_params())
    return inv_list


def frontier(region: str):
    FRONTIER_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/nissan/frontier/{region}'
    return scrape_url(FRONTIER_4WD_URL, default_truck_params())


def gx460(region: str):
    GX460_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/lexus/gx-460/{region}'
    return scrape_url(GX460_URL, default_suv_params())


def odyssey(region: str):
    ODYSSEY_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/honda/odyssey/{region}'
    return scrape_url(ODYSSEY_URL, default_params())


def ram(region: str):
    '''ignores V6 models'''
    RAM_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/ram/1500/{region}'
    params = default_truck_params()
    params[ENGINE_CYL_KEY] = ENGINE_CYL_8
    return scrape_url(RAM_4WD_URL, params)


# def sedona(region: str):
#     SEDONA_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/kia/sedona/{region}'
#     return scrape_url(SEDONA_URL, default_params())


def sienna(region: str):
    SIENNA_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/toyota/sienna/{region}'
    return scrape_url(SIENNA_URL, default_params())


def sierra(region: str):
    SIERRA_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/gmc/sierra-1500/{region}'
    return scrape_url(SIERRA_URL, default_truck_params())


def sequoia(region: str):
    SEQUOIA_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/toyota/sequoia/{region}'
    return scrape_url(SEQUOIA_4WD_URL, default_suv_params())


def silverado(region: str):
    SILVERADO_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/silverado-1500/{region}'
    return scrape_url(SILVERADO_4WD_URL, default_truck_params())


def suburban(region: str):
    SUBURBAN_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/suburban/{region}'
    return scrape_url(SUBURBAN_4WD_URL, default_suv_params())


def tacoma(region: str):
    TACOMA_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/toyota/tacoma/{region}'
    return scrape_url(TACOMA_4WD_URL, default_truck_params())


def tahoe(region: str):
    TAHOE_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/chevrolet/tahoe/{region}'
    return scrape_url(TAHOE_4WD_URL, default_suv_params())


def titan(region: str):
    TITAN_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/nissan/titan/{region}'
    params = default_truck_params()
    params[SEARCH_RADIUS_KEY] = 500  # fewer titans around
    params[MIN_YEAR_KEY] = '2016'  # updated body style
    return scrape_url(TITAN_4WD_URL, params)


def tundra(region: str):
    TUNDRA_4WD_URL = f'https://www.autotrader.com/cars-for-sale/all-cars/awd-4wd/toyota/tundra/{region}'
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


def default_suv_params():
    '''SUVs are in lower quantity, so relax query'''
    params = default_params()
    params[SEARCH_RADIUS_KEY] = 500
    params[MAX_MILEAGE_KEY] = 200_000
    return params


def scrape_url(base_url: str, params: dict, dbug=False):
    '''Scrapes specified AutoTrader URL'''
    resp = send_req(base_url, params, dbug=dbug)
    inv_list, next_skip = scrape_doc(resp)

    while next_skip:
        dur = randint(10, 30)
        print(f'scraping next page in {dur} secs')
        time.sleep(dur)
        params[SKIP_KEY] = next_skip
        resp = send_req(base_url, params, dbug=dbug)
        next_list, next_skip = scrape_doc(resp, dbug=dbug)
        inv_list += next_list

    if dbug:
        with open('diags/inventory_list.json', 'w+') as file:
            json.dump(inv_list, file)

    return inv_list


def send_req(base_url: str, params: dict, dbug=False):
    client = httpx.Client(timeout=120)  # long, but not infinite
    req = httpx.Request('GET', base_url, params=params, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',

    })
    # print(f'[DEBUG] about to send request: {req}')
    resp = client.send(req)
    if dbug:
        with open('diags/response.html', 'w+') as file:
            file.write(resp.text)

    if resp.status_code > 299:
        raise Exception(f'request failed with status code: {resp.status_code}')

    return resp.text


def scrape_doc(document: str, dbug=False):
    '''Scrapes an AutoTrader HTML document containing vehicle search results '''
    DATA_LOC = 'window.__BONNET_DATA__'
    bs = BeautifulSoup(document, 'html.parser')
    data = bs.find('script', text=re.compile(DATA_LOC)).get_text()
    payload = data.split(DATA_LOC + '=')[1]
    if dbug:
        with open('diags/response_data.json', 'w+') as file:
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
