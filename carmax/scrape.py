import json
from urllib.parse import urlencode
import httpx
import random
from time import sleep

# common filters
FILTER_FOUR_WHEEL_DRIVE = '4wdawd'
FILTER_CREW_CAB = '4d-crew-cab'


def all_queries():
    '''convenience helper for querying all models with default filters'''
    return (
        ('chevrolet', 'colorado', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('chevrolet', 'silverado-1500',
         (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('chevrolet', 'suburban', (FILTER_FOUR_WHEEL_DRIVE)),
        ('chevrolet', 'tahoe', (FILTER_FOUR_WHEEL_DRIVE)),
        ('ford', 'expedition', (FILTER_FOUR_WHEEL_DRIVE)),
        ('ford', 'f150', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('honda', 'odyssey', []),
        ('nissan', 'frontier', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('nissan', 'titan', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('ram', '1500', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('toyota', 'tacoma', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('toyota', 'tundra', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
    )


def api(queries: list, chunk_size=100, dbug=False):
    '''
    scrapes the carmax API.  
        `queries` must be a 3-tuple with the following components:
            [0]: make
            [1]: model
            [2]: filters to search on
    '''
    for q in queries:
        yield model(q[0], q[1], *q[2], chunk_size=chunk_size, dbug=dbug)


def model(make, model, *filters, chunk_size=100, dbug=False):
    '''
    scrapes the carmax API for a specific make/model.  
        `filters` are features to search on (e.g. 4wdawd, 4d-crew-cab, etc...)
        `chunk_size` specifies how many listings to retrieve per iteration
    '''
    skip = 0
    while True:
        resp = send_req(make, model, *filters, skip=skip, take=chunk_size, dbug=dbug)
        listings = parse_resp(resp)
        yield listings
        if len(listings) < chunk_size:
            break
        skip += chunk_size
        sleep_dur = random.randint(10, 30)
        print(f'sleeping for {sleep_dur} seconds')
        sleep(sleep_dur)


def send_req(make, model, *filters, skip=0, take=100, dbug=False):
    if filters is None:
        filters = []

    search = f'/cars/{make}/{model}'
    for f in filters:
        search += f'/{f}'

    print(f'search filter: {search}')
    with httpx.Client(timeout=120) as client:
        attempt = 0
        while True:
            try:
                attempt += 1
                resp = client.get(
                    f'https://www.carmax.com/cars/api/search/run?uri={search}&year=2016-2023&price=50000&skip={skip}&take={take}&radius=radius-nationwide&shipping=-1',
                    headers={
                        'Cookie': 'KmxSession_0=SessionId=3a643f5c-9093-4138-af23-39d3c2db80c2&logOdds=1.749343&logOddsA=-1.3124279159999999&logOddsI=0.8170897999999999; KmxStore=StoreId=6031; KmxVisitor_0=StoreId=6031&Zip=30523&Lat=34.713154&Lon=-83.551309&ZipConfirmed=True&ZipDate=6/17/2023 12:19:08 PM&VisitorID=813d3095-16d6-4bad-9287-0eb43afb7d3b&CookieDate=2/2/2023 3:20:27 AM&IsFirstVisit=False; _abck=8261582D852BF143C3DFDD6532142EA0~-1~YAAQXA3eF5GtEryIAQAArYBLyQqI1hjhQfmWj+wpmnsWDFHMppuHxGqALt4IqFMKnr4HLebICPleNiA0shkPaSbP2ZKj5S0H1syPfwdK3BjeVVkneO4uJ7bC+RW5HHWby1EKW+06bhAZJg4AsgaoG39/2BX+fzBRxoov+cGTjE1NzaksCU6CnRFMPvIN7Wdakrg7246KqR/YUhXPt/4wW0mdx57yKv008oMNFqoNArxUOz+qNryNyKTm+Ikq01dsuXwYzAv+yAPtZmehh6QkPJ6GqFYso1im4NbINWxJe3GBdJY7Y69JiDOWONbNWL3AiRDjHinw4uJZmKvCYCRnN0g15D9z+bN0f6dWzp7Y3c7sp9WsDx03psP23Bi31lC/onrEPph4Dg==~-1~-1~1675311518; ak_bmsc=77F53C6FA090A066C8B642929BFE9EED~000000000000000000000000000000~YAAQXA3eF5KtEryIAQAArYBLyRSs1sKYj853dHyy9l1DhuIzR/E65BQ9JWs/bnmGL8IjhCMO/dsGviwPOlhKGBA8ddg63UkImj9jNZq88k4ss6NQ9XooeBumnppcYGzbaGcPBlKrmR1m8yENKpNok1SQdkw2dqgIkMvPpVhbiC016VUAV5nss6yahV3+RnE+P+g165lrkwnvDEig4jjk2gvikx7ooZrbpWCe/J2rE+iRa4BQbQRpctiNaVNcim81N9YZMFbal0GGXehjx2H4yeRuXj+Qr0WMDIvEQU6YB7A8i596U/fw4wgoWak3sCD5I34xcuSeqYID2Y9W/QDmI/P3HoIZwR9c3lboycJ8pNHAbQMazasyg5DX0o4=; bm_sz=08668385718CE9C15E5D6770E05B2517~YAAQXA3eF5OtEryIAQAArYBLyRTDpxsmX6OW066q3TohqGpUzN+lOogzNHIfeGZwTtVLN1auK1RwNsPEfXKthktPqzjzEfiIsxY65fMJ7Pic9vt/qMurSWNwtsLq3uIYj3KHw5zgCA5Zwt/9Vntq0dCH5zi7hpXDEptlcxIrTkKtsORQ2Jqv+2WEIN8MXRrOpy5n2CKLwcTVLHigARSQgORqnu8iIOog7WOFkLz9Mw41B7sNKv4Dpqz2Nnegoa04vJJHeZOVQgXW5pebR8iBMaE13dwzxU+NyC1jo6ClcqeJYa8=~4535604~3555641',
                        # fails with Mozilla, but works with Postman... wtf
                        'User-Agent': 'PostmanRuntime/7.30.0',
                    })

                break
            except Exception as e:
                print(
                    f'[attempt #{attempt}] encountered problem while sending request: {e}')
                
                if attempt > 2:
                    raise e

    print('completed request')
    respjson = resp.json()
    if dbug:
        with open('data/response.json', 'w+') as file:
            json.dump(respjson, file)

    return respjson


def parse_resp(respjson):
    items = []
    for i in respjson['items']:
        items.append({
            'body':         i['body'].lower(),
            'carmax_id':    i['stockNumber'],
            'city':         i['storeCity'].lower(),
            'color':        i['exteriorColor'].lower(),
            'drive_type':   i['driveTrain'].lower(),
            'engine_cyl':   _attr('cylinders', int, i),
            'engine_size':  _attr('engineSize', str, i),
            'engine_type':  _attr('engineType', str, i),
            'features':     i['features'],
            'highlights':   i['highlights'],
            'make':         i['make'].lower(),
            'mileage':      i['mileage'],
            'model':        i['model'].lower(),
            'mpg_city':     _attr('mpgCity', int, i),
            'mpg_hwy':      _attr('mpgHighway', int, i),
            'msrp':         _attr('msrp', int, i),
            'packages':     i['packages'],
            'price':        int(i['basePrice']),
            'prior_uses':   [int(p) for p in i['priorUses']],
            'state':        i['stateAbbreviation'].lower(),
            'store_id':     i['storeId'],
            'trim':         _attr('trim', str, i),
            'vin':          i['vin'],
            'year':         i['year'],
            'zip':          _attr('storeZip', str, i),
        })

    return items


def _attr(key: str, valtype, listing: dict):
    '''get nullable value from listing'''
    try:
        m = listing[key]
        if m is None:
            return

        if valtype is str:
            return m.lower()
        elif valtype is int:
            return int(m)
        else:
            raise Exception(f'unexpected valtype "{valtype}"')

    except KeyError as e:
        pass
    except Exception as e:
        print(f'[{listing["vin"]}] cannot find "{key}": {e}')
        raise e
